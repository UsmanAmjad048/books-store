from django.middleware.csrf import get_token
from django.http import JsonResponse
from .models import Bookstore
from .api.serializers import BooksSerializer
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .api.serializers import BooksSerializer
from .form import AddBooksForm
from django.views import View
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .authentication import CustomTokenAuthentication
from django.shortcuts import get_object_or_404


def books(request):
    books = Bookstore.objects.all()
    serializer = BooksSerializer(books, many=True)
    return JsonResponse(serializer.data, safe=False)

def booksuserid(request, user_id, book_id):
    try:
        book = get_object_or_404(Bookstore, id=book_id, user=user_id)
        serializer = BooksSerializer(book)
        return JsonResponse(serializer.data)
    except Bookstore.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

class AddBooksView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, book_id=None):
        if book_id is not None:
            try:
                book = Bookstore.objects.get(id=book_id, user=user_id)
                serializer = BooksSerializer(book)
                return Response(serializer.data)
            except Bookstore.DoesNotExist:
                return JsonResponse({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            books = Bookstore.objects.filter(user=user_id)
            serializer = BooksSerializer(books, many=True)
            return Response(serializer.data)

    def post(self, request):
        form = AddBooksForm(request.data)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            serializer = BooksSerializer(book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, book_id):
            try:
                book = Bookstore.objects.get(id=book_id)
                if book.user != request.user:
                    return JsonResponse({'error': 'You do not have permission to delete this book'}, status=403)
                book.delete()
                return JsonResponse({'message': 'Book deleted successfully'}, status=204)
            except Bookstore.DoesNotExist:
                return JsonResponse({'error': 'Book not found'}, status=404)