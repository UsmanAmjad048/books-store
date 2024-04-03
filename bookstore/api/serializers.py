from rest_framework import serializers
from ..models import Bookstore



class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookstore
        fields = '__all__'
    
class CustomBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookstore
        exclude = ['image']

    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None
