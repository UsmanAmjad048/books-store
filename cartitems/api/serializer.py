from rest_framework import serializers
from ..models import CartItem, CartItemBook

class CartItemBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItemBook
        exclude = ['cart_item']

class CartItemSerializer(serializers.ModelSerializer):
    cart_items = CartItemBookSerializer(many=True)

    class Meta:
        model = CartItem
        fields = ('id','user', 'shipping_number', 'shipping_address', 'date_added', 'status', 'cart_items')

    def create(self, validated_data):
        cart_items_data = validated_data.pop('cart_items')
        cart_item = CartItem.objects.create(**validated_data)
        for cart_item_data in cart_items_data:
            CartItemBook.objects.create(cart_item=cart_item, **cart_item_data)
        return cart_item
    
class CartItemBookSerializers(serializers.ModelSerializer):
    class Meta:
        model = CartItemBook
        fields = "__all__"
