from django.db import models
from .enums import *


class BaseModel(models.Model):
    """
    Description: An abstract base model that provides common fields for other models, such as created_at and updated_at.

    :Fields:
    - created_at: A DateTimeField that stores the date and time of creation automatically.
    - updated_at: A DateTimeField that stores the date and time of the last update automatically.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Topping(models.Model):
    """
    Description: Model to represent pizza toppings.

    :Fields:
    - name: A CharField to store the name of the topping.
    - price: An IntegerField to store the price of the topping.

    :Methods:
    - __str__: Returns the name of the topping as its string representation.
    """

    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Order(BaseModel):
    """
    Description: Model to represent pizza orders.

    :Fields:
    - timestamp: A DateTimeField that stores the date and time of the order.
    - total: A DecimalField that stores the total cost of the order.
    - in_cart: A BooleanField to indicate if the order is in the cart.
    - placed: A BooleanField to indicate if the order has been placed.
    - status: A CharField with choices to represent the order status.
    - completed: A BooleanField to indicate if the order has been completed.

    :Methods:
    - __str__: Returns a string representation of the order, including its ID.
    """

    timestamp = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    in_cart = models.BooleanField(default=True)
    placed = models.BooleanField(default=False)
    status = models.CharField(choices=ORDER_STATUS_CHOICE, max_length=100, null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'Order #{self.id}'


class Pizza(BaseModel):
    """
    Description: Model to represent pizza items in an order.

    :Fields:
    - order: A ForeignKey to associate the pizza with an order.
    - base_type: A CharField with choices to represent the base type of the pizza.
    - cheese_type: A CharField with choices to represent the cheese type of the pizza.
    - toppings: A ManyToManyField to associate toppings with the pizza.
    - description: A TextField to store a description of the pizza.
    - total: An IntegerField to store the total cost of the pizza.
    - is_deleted: A BooleanField to indicate if the pizza has been deleted.

    :Methods:
    - __str__: Returns a string representation of the pizza, including its ID.
    """

    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    base_type = models.CharField(max_length=100, choices=BASE_CHOICES, null=False, blank=False)
    cheese_type = models.CharField(max_length=100, choices=CHEESE_CHOICES, null=False, blank=False)
    toppings = models.ManyToManyField(
        Topping,  # To allow relationships with the same model
        blank=True,
        null=True
    )
    description = models.TextField()
    total = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'Pizza #{self.id}'
