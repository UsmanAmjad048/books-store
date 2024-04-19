from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from bookstore.models import Bookstore
from cartitems.models import CartItem ,CartItemBook



class Notification(models.Model):
    cartitem_id = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name='cartitems_id')
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    purchaserid = models.ForeignKey(User, on_delete=models.CASCADE ,related_name='notifications_as_purchaser')
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE , related_name='notifications_as_seller')



    def __str__(self):
        return self.title
        
        
        