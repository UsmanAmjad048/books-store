from django.urls import path
from . import views


urlpatterns = [
    path('addcart/', views.AddCartAPIView.as_view(), name='addcart'),
]
