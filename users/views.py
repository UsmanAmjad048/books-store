from django.http import JsonResponse
from django.contrib.auth.models import User
from .api.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from .api.serializers import UserSignupSerializer
from django.contrib.auth import authenticate
import secrets
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.middleware.csrf import get_token
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from bookstore.authentication import CustomTokenAuthentication
from rest_framework.response import Response
from django.core.mail import send_mail
from django.template.loader import render_to_string

def index(request):
    if request.user.is_superuser:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'message': 'You are not a superuser'}, status=403)

def indexid(request, user_id):
    if request.user.is_superuser:
        user = get_object_or_404(User, id=user_id)
        user.is_superuser = False
        user.save()
        serializer = UserSerializer(user)
        return JsonResponse({'message': 'You are not a superuser'},serializer.data)
    else:
        user = get_object_or_404(User, id=user_id)
        user.is_superuser = True
        user.save()
        serializer = UserSerializer(user)
        return JsonResponse({'message': 'You are  a superuser'},serializer.data)

class SignUpView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer



@csrf_exempt
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)

                return JsonResponse({'token': token.key , 'issuperuser':request.user.is_superuser , 'user_id':request.user.id , 'is_staff': request.user.is_staff})
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        else:
            return JsonResponse({'error': 'your account not active or invalid username and password'}, status=400)
    else:
        form = AuthenticationForm()
        return JsonResponse({'form': form})


def generate_access_token(user):
    access_token = secrets.token_hex(16)
    return access_token
@csrf_exempt
def custom_logout(request):
    logout(request)
    return JsonResponse({'message': 'You have been logged out successfully'})

class InactiveUsersView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            inactive_users = User.objects.filter(is_active=False)
            serializer = UserSerializer(inactive_users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You are not a staff'}, status=status.HTTP_403_FORBIDDEN)

@csrf_exempt
def activate_user(request, user_id):
    if request.method == 'POST':
        try:
            user = User.objects.get(pk=user_id)
            subject = 'Account Activation Notification'
            message = render_to_string('email/account_activate_email.txt', {'username': user.username})
            from_email = '1999usmanamjad@gmail.com'  
            to_email = [user.email]
            send_mail(subject, message, from_email, to_email)
            user.is_active = True
            user.save()
            return JsonResponse({'message': 'User activated successfully'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

@csrf_exempt
def delete_user(request, user_id):
    if request.method == 'DELETE':
        try:
            user = User.objects.get(pk=user_id)
            subject = 'Account Deletion Notification'
            message = render_to_string('email/account_deleted_email.txt', {'username': user.username})
            from_email = '1999usmanamjad@gmail.com'  
            to_email = [user.email]
            send_mail(subject, message, from_email, to_email)
            user.delete()
            return JsonResponse({'message': 'User deleted successfully'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)
    else:
        return JsonResponse({'error': 'Only DELETE method is allowed'}, status=405) 


