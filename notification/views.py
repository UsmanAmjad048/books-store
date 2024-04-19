from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .api.serializers import NotificationSerializer
from .models import Notification
from rest_framework.permissions import IsAuthenticated
from bookstore.authentication import CustomTokenAuthentication
from cartitems.models import CartItem, CartItemBook
from cartitems.api.serializer import CartItemBookSerializers, CartItemSerializer
from django.db.models import Q
from django.http import Http404


class notificationApi(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            notifications = Notification.objects.filter(
                seller_id=request.user, is_read=False).order_by('-created_at')
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        data = request.data
        notification_id = data.get('id')
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.is_read = True
            notification.save()
            notifications = Notification.objects.filter(
                seller_id=request.user, is_read=False).order_by('-created_at')
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class notificationorder(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            if user.is_superuser:
                cartid = request.GET.get('cart_item_value')
                if cartid:
                    try:
                        cart_items = CartItemBook.objects.filter(
                            seller_id=user.id, cart_item_id=cartid)
                        serializer = CartItemBookSerializers(
                            cart_items, many=True)

                        cart_item = CartItem.objects.get(id=cartid)
                        cart_item_serializer = CartItemSerializer(cart_item)

                        return Response({'cart_items': serializer.data, 'cart_item': cart_item_serializer.data}, status=status.HTTP_200_OK)
                    except CartItem.DoesNotExist:
                        raise Http404("CartItem does not exist")
                    except CartItemBook.DoesNotExist:
                        raise Http404("CartItemBook does not exist")
                else:
                    cart_items = CartItemBook.objects.filter(seller_id=user.id)
                    serializer = CartItemBookSerializers(cart_items, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                cart_items = CartItem.objects.filter(
                    (Q(status="pending") | Q(status="dispatch")))
                serializer = CartItemSerializer(cart_items, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class notiorderid(APIView):

#     def get(self, request, *args, **kwargs):
#         try:
#             id = kwargs.get('id')
#             cart_items = CartItem.objects.filter(id=id)
#             serializer = CartItemSerializer(cart_items, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderComplete(APIView):

    def post(self, request, *args, **kwargs):
        try:
            cartorderid = kwargs.get('id')
            data = request.data
            status = data.get('status')
            cart_items = CartItem.objects.filter(id=cartorderid)
            for cart_item in cart_items:
                cart_item.status = status
                cart_item.save()
        except Exception as e:
            pass
