# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class AddCartAPIView(APIView):
    def post(self, request):
        book_id = request.data.get('book_id')
        quantity = request.data.get('quantity')
        return Response({'message': 'Item added to cart successfully'}, status=status.HTTP_201_CREATED)
