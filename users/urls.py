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
    path('inactive_users/', views.InactiveUsersView.as_view(), name='inactive_users'),
    path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
]
