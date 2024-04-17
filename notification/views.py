from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .api.serializers import NotificationSerializer
from .models import Notification
from rest_framework.permissions import IsAuthenticated
from bookstore.authentication import CustomTokenAuthentication
from cartitems.models import CartItem , CartItemBook
from cartitems.api.serializer import CartItemBookSerializers , CartItemSerializer

class notificationApi(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            notifications = Notification.objects.filter(seller_id=request.user, is_read=False).order_by('-created_at')
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
            notifications = Notification.objects.filter(seller_id=request.user, is_read=False).order_by('-created_at')
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
            cart_items = CartItemBook.objects.filter(seller_id=request.user.id)
            serializer = CartItemBookSerializers(cart_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class notiorderid(APIView):

    def get(self, request, *args, **kwargs):
        try:
            id = kwargs.get('id')
            cart_items = CartItem.objects.filter(id=id)
            serializer = CartItemSerializer(cart_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ordercomplete(APIView):

    def get(self, request, *args, **kwargs):
        try:
            cart_items = CartItemBook.objects.filter(seller_id=request.user.id)
            serializer = CartItemBookSerializers(cart_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)