from django import forms
from .models import Bookstore


class AddBooksForm(forms.ModelForm):
    class Meta:
        model = Bookstore
        fields = ['title', 'description', 'author', 'stock', 'image','price',]


