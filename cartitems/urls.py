from django.urls import path
from .views import AddCartAPIView # Import the correct view

urlpatterns = [
    path('addcart/', AddCartAPIView.as_view(), name='addcart'),  # Use .as_view() to register the view
    path('purchase-history/', AddCartAPIView.as_view(), name='purchase-history'),  # Use .as_view() to register the view

]
