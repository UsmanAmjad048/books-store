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
# from django.contrib.auth.models import User

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
                
                return JsonResponse({'token': token.key , 'issuperuser':request.user.is_superuser , 'user_id':request.user.id})
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        else:
            return JsonResponse({'error': 'Form is not valid'}, status=400)
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


# def promote_to_superuser(username):
#     try:
#         user = User.objects.get(username=username)

#         user.is_superuser = True
#         user.is_staff = True
#         user.save()

#         print(f"User '{username}' has been promoted to superuser.")
#     except User.DoesNotExist:
#         print(f"User '{username}' does not exist.")

