from django.urls import path
from . import views
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView
# )
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('users/', views.index, name='index'),
    path('users/<int:user_id>/', views.indexid, name='indexid'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.custom_login, name='login_view'),
    path('logout/', views.custom_logout, name='logout_view'),
    # path('promote_to_superuser/', views.promote_to_superuser, name='promote_to_superuser'),
]
