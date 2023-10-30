from rest_framework import serializers
from .models import Order, Topping

class ToppingSerializer(serializers.ModelSerializer):
    """
    Description: A serializer for Topping model, used to convert Topping instances to JSON representation and vice versa.

    :Meta:
    - model: The model class to serialize.
    - fields: '__all__' to include all fields from the model.

    :methods
    - get_toppings_name: A custom method to retrieve the names of associated toppings.
    """

    class Meta:
        model = Topping
        fields = '__all__'

    # def get_toppings_name(self, instance):
    #     toppings = instance.toppings.all()
    #     return [str(topping.name) for topping in toppings]

class OrderSerializer(serializers.ModelSerializer):
    """
    Description: A serializer for Order model, used to convert Order instances to JSON representation and vice versa.

    :Meta:
    - model: The model class to serialize.
    - fields: '__all__' to include all fields from the model.
    """

    class Meta:
        model = Order
        fields = '__all__'

class PizzaSerializer(serializers.ModelSerializer):
    """
    Description: A serializer for Pizza model, used to convert Pizza instances to JSON representation and vice versa.

    :Meta:
    - model: The model class to serialize.
    - fields: '__all__' to include all fields from the model.

    :fields
    - toppings: A SerializerMethodField to include toppings' names in the serialized representation.

    :methods
    - get_toppings_name: A custom method to retrieve the names of associated toppings for the pizza.
    """

    toppings = serializers.SerializerMethodField('get_toppings_name', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_toppings_name(self, instance):
        """
        Description: Custom method to retrieve the names of associated toppings for the pizza.

        :param instance: The Pizza instance for which to retrieve toppings.

        :return: (list) A list of topping names as strings.
        """
        toppings = instance.toppings.all()
        return [str(topping.name) for topping in toppings]
