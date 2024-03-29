from django.contrib.auth.models import User
from django.db import models
from bookstore.models import Bookstore 


class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Bookstore, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.user.username}'s cart item: {self.book.title}"
