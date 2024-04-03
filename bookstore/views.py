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
from rest_framework.parsers import MultiPartParser
from django.db.models import Q
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def books(request):
    books_list = Bookstore.objects.all().order_by('-created_date')
    paginator = Paginator(books_list, 5)  # Change 10 to the number of items per page you desire
    page = request.GET.get('page')  # Get the current page number from the request
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        books = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        books = paginator.page(paginator.num_pages)
    serializer = BooksSerializer(books, many=True)
    return JsonResponse({
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'current_page': books.number,
        'next_page': books.next_page_number() if books.has_next() else None,
        'previous_page': books.previous_page_number() if books.has_previous() else None,
        'results': serializer.data
    }, safe=False)

@csrf_exempt
def SearchBooksAPIView(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query', '')  # Use get() method to avoid KeyError
            books_list = Bookstore.objects.filter(title__icontains=query).order_by('-created_date')
            paginator = Paginator(books_list, 5)  # Change 5 to the number of items per page you desire
            page = request.GET.get('page')  # Get the current page number from the request
            try:
                books = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                books = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                books = paginator.page(paginator.num_pages)
            serializer = BooksSerializer(books, many=True)
            return JsonResponse({
                'count': paginator.count,
                'num_pages': paginator.num_pages,
                'current_page': books.number,
                'next_page': books.next_page_number() if books.has_next() else None,
                'previous_page': books.previous_page_number() if books.has_previous() else None,
                'results': serializer.data
            }, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)  # Return error response
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)  # Return method not allowed error


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
    parser_classes = [MultiPartParser]

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
        image_file = request.data.get('image')
        request_data = request.data.copy()
        del request_data['image']

        form = AddBooksForm(request_data, request.FILES)

        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user

            book.save()

            if image_file:
                book.image = image_file
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
