from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CartItem
from .api.serializer import CartItemSerializer
from rest_framework.permissions import IsAuthenticated
from bookstore.authentication import CustomTokenAuthentication
from bookstore.models import Bookstore

class AddCartAPIView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Add items to the user's cart.
        """
        try:
            print(request.data)
            user = request.user
            cart_items_data = request.data.get('cartItems', []) 
            serializer = CartItemSerializer(data={'shipping_number': request.data['shippingNumber'], 
                                                   'shipping_address': request.data['shippingAddress'],
                                                   'cart_items': cart_items_data,
                                                   'user': user.id}, 
                                              context={'request': request})
            if serializer.is_valid():
                serializer.save(user=user) 
                # here we need to bookmowernuser database decrice stoke value 
                # for each book in the cart
                for cart_item_data in cart_items_data:
                    book = Bookstore.objects.get(id=cart_item_data['book'])
                    book.stock -= cart_item_data['quantity']
                    book.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request, *args, **kwargs):
        """
        Get the user's cart items.
        """
        try:
            user = request.user
            cart_items = CartItem.objects.filter(user=user)
            serializer = CartItemSerializer(cart_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
