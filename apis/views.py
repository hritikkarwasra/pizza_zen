import time
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *
from .enums import *
from celery import shared_task
import datetime


@shared_task
def switch_to_preparing(order_id):
    """
    Description: This function is a Celery task that changes the status of an order to "Preparing" and is called with a delay.

    :param order_id: (int) The ID of the order to be prepared.

    :return: (bool) True if the operation was successful.
    """
    now = datetime.datetime.now()
    cart = Order.objects.get(id=order_id)
    cart.status = PREPARING
    cart.save()
    return True


@shared_task
def switch_to_dispatch(order_id):
    """
    Description: This function is a Celery task that changes the status of an order to "Dispatched."

    :param order_id: (int) The ID of the order to be dispatched.

    :return: (bool) True if the operation was successful.
    """
    now = datetime.datetime.now()
    now()
    cart = Order.objects.get(id=order_id)
    cart.status = DISPATCHED
    cart.save()
    return True


@shared_task
def switch_to_delivered(order_id):
    """
    Description: This function is a Celery task that changes the status of an order to "Delivered."

    :param order_id: (int) The ID of the order to be marked as delivered.

    :return: (bool) True if the operation was successful.
    """
    now = datetime.datetime.now()
    cart = Order.objects.get(id=order_id)
    cart.status = DELIVERED
    cart.completed = True
    cart.save()
    return True


@shared_task
def switch_status(order_id):
    """
    Description: This function is a Celery task that orchestrates the order status transition from "Preparing" to "Delivered" with delays.

    :param order_id: (int) The ID of the order to update.

    :return: (bool) True if the operation was successful.
    """
    switch_to_preparing.apply_async([order_id], countdown=60)
    switch_to_dispatch.apply_async([order_id], countdown=180)
    switch_to_delivered.apply_async([order_id], countdown=300)
    return True


class OrdersViewSet(viewsets.ModelViewSet):
    """
    Description: A viewset for managing orders. It provides functionality to create, retrieve, update, and delete orders.

    Functions:
    - place_order: Places an order with the specified order ID and triggers status transitions using Celery.

    :attributes
    - queryset: Queryset for retrieving orders.
    - serializer_class: Serializer class for orders.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(methods=['POST'], detail=False)
    def place_order(self, request, *args, **kwargs):
        """
        Description: Places an order with the specified order ID and triggers status transitions using Celery.

        :param request: (HttpRequest) HTTP request object.
        :param args: (tuple) Additional positional arguments.
        :param kwargs: (dict) Additional keyword arguments.

        :return: (Response) Response object with a success message.
        """
        order_id = self.request.query_params.get('id')
        try:
            cart = Order.objects.get(id=order_id)
            cart.status = ACCEPTED
            cart.placed = True
            cart.save()
        except Order.DoesNotExist:
            return Response({"msg": "Invalid Order id"}, status=status.HTTP_400_BAD_REQUEST)
        switch_status.delay(order_id)
        return Response({'msg': 'Order Placed Successfully'}, status=status.HTTP_202_ACCEPTED)


class PizzaViewSet(viewsets.ModelViewSet):
    """
    Description: A viewset for managing pizza items. It provides functionality to create, retrieve, update, and delete pizza items in the cart.

    Functions:
    - add_pizza_to_cart: Adds a pizza to the cart with toppings and calculates the total price.
    - remove_pizza_from_cart: Removes a pizza from the cart and updates the total price.

    :attributes
    - queryset: Queryset for retrieving pizza items.
    - serializer_class: Serializer class for pizza items.
    """

    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer

    @action(methods=['POST'], detail=False)
    def add_pizza_to_cart(self, request, *args, **kwargs):
        """
        Description: Adds a pizza to the cart with toppings and calculates the total price.

        :param request: (HttpRequest) HTTP request object.
        :param args: (tuple) Additional positional arguments.
        :param kwargs: (dict) Additional keyword arguments.

        :return: (Response) Response object with a success message.
        """
        data = self.request.data
        toppings = data.pop('toppings', None)
        if toppings and len(toppings) > 5:
            return Response({"msg": "Only 5 toppings allowed."}, status=status.HTTP_400_BAD_REQUEST)
        base_prices = dict(BASE_CHOICES_PRICES)
        cheese_type_prices = dict(CHEESE_CHOICES_PRICES)
        base = data.get('base_type')
        cheese_type = data.get('cheese_type')
        total = base_prices[base] + cheese_type_prices[cheese_type]
        toppings_qs = Topping.objects.filter(id__in=toppings)
        topping_total = 0
        for topping in toppings_qs:
            topping_total += topping.price
        total += topping_total
        try:
            order_id = data.pop('order_id', None)
            cart = Order.objects.get(id=order_id)
            if cart:
                cart.total += total
            cart.save()
        except Order.DoesNotExist:
            cart = Order(total=total)
            cart.save()
        data['order'] = cart
        data['total'] = total
        pizza = Pizza.objects.create(**data)
        pizza.toppings.set(toppings)
        return Response({"response": f"Pizza Successfully added to {cart.id}"}, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False)
    def remove_pizza_from_cart(self, request, *args, **kwargs):
        """
        Description: Removes a pizza from the cart and updates the total price.

        :param request: (HttpRequest) HTTP request object.
        :param args: (tuple) Additional positional arguments.
        :param kwargs: (dict) Additional keyword arguments.

        :return: (Response) Response object with a success message.
        """
        pizza_id = self.request.query_params.get('id', None)
        if pizza_id is None:
            return Response({"msg": "Invalid Pizza, Pls Try Again"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            pizza = Pizza.objects.get(id=pizza_id)
        except Pizza.DoesNotExist:
            return Response({"msg": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)
        cart = pizza.order
        cart.total -= pizza.total
        cart.save()
        pizza.is_deleted = True
        pizza.save()
        return Response({"msg": f"Pizza Removed Successfully updated price {cart.total}"},
                        status=status.HTTP_202_ACCEPTED)
