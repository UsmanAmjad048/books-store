from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Bookstore(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_date = models.DateField(default=date.today)
    author = models.CharField(max_length=100)
    stock = models.IntegerField(default = 1)
    total_books = models.IntegerField(default = 0)
    category = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='cover_photo/', null=True, blank=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title
    
    @property
    def total_sold(self):
        return self.total_books - self.stock
    
    @property
    def total_available(self):
        return self.stock
    @property
    def total_earnings(self):
        return self.price * self.total_sold