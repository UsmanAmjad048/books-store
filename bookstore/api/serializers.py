from rest_framework import serializers
from ..models import Bookstore



class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookstore
        fields = '__all__'
    
