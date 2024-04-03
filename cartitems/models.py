from django.contrib.auth.models import User
from django.db import models
from bookstore.models import Bookstore

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_number = models.CharField(max_length=100)
    shipping_address = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"{self.user.username}'s cart item"

class CartItemBook(models.Model):
    cart_item = models.ForeignKey(CartItem, related_name='cart_items', on_delete=models.CASCADE)
    book = models.ForeignKey(Bookstore, on_delete=models.CASCADE)
    booktitle = models.CharField(max_length=255, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.cart_item.user.username}'s cart item: {self.book.title}"