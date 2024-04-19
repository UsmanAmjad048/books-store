from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CartItem
from .api.serializer import CartItemSerializer
from rest_framework.permissions import IsAuthenticated
from bookstore.authentication import CustomTokenAuthentication
from bookstore.models import Bookstore
from notification.api.serializers import NotificationSerializer
from django.db.models import Q
 


class AddCartAPIView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Add items to the user's cart.
        """
        try:
            user = request.user
            cart_items_data = request.data.get('cartItems', [])
            sellerid = request.data.get('seller_id', None)

            serializer = CartItemSerializer(data={
                'shipping_number': request.data['shippingNumber'],
                'shipping_address': request.data['shippingAddress'],
                'cart_items': cart_items_data,
                'user': user.id,
                'seller_id': sellerid
            }, context={'request': request})

            if serializer.is_valid():
                data = serializer.save(user=user)
                cartid = data.id
                for cart_item_data in cart_items_data:
                    try:
                        book = Bookstore.objects.get(id=cart_item_data['book'])
                        book.stock -= cart_item_data['quantity']
                        book.save()
                        cart_item_user_id = cart_item_data['bookuser']
                        cart_item_booktitle = cart_item_data['booktitle']

                        try:
                            serializerfornotification = NotificationSerializer(data={
                                'title': cart_item_booktitle,
                                'is_read': False,
                                'purchaserid': user.id,
                                'seller_id': cart_item_user_id,
                                'cartitem_id': cartid
                            })

                            serializerfornotification.is_valid()
                            serializerfornotification.save()

                        except Exception as e:
                            pass

                        
                    except Bookstore.DoesNotExist:
                        pass
                user_order_noti = NotificationSerializer(data={
                            'title': "Your order preparation is starting. You will be notified of your order.",
                            'is_read': False,
                            'purchaserid': user.id,
                            'seller_id': user.id,
                            'cartitem_id': cartid
                        })

                user_order_noti.is_valid(raise_exception=True)
                user_order_noti.save()

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
            cart_items = CartItem.objects.filter(
                Q(user=user))
            serializer = CartItemSerializer(cart_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
