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
from rest_framework.pagination import PageNumberPagination


def books(request):
    books_list = Bookstore.objects.all().order_by('-created_date')
    # Change 10 to the number of items per page you desire
    paginator = Paginator(books_list, 5)
    # Get the current page number from the request
    page = request.GET.get('page')
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
            books_list = Bookstore.objects.filter(
                title__icontains=query).order_by('-created_date')
            # Change 5 to the number of items per page you desire
            paginator = Paginator(books_list, 5)
            # Get the current page number from the request
            page = request.GET.get('page')
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
            # Return error response
            return JsonResponse({'error': str(e)}, status=400)
    else:
        # Return method not allowed error
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def booksuserid(request, user_id, book_id):
    try:
        book = get_object_or_404(Bookstore, id=book_id, user=user_id)
        serializer = BooksSerializer(book)
        return JsonResponse(serializer.data)
    except Bookstore.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)


class DashBoardData(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:    
            user_id = request.user.id
            bookstores = Bookstore.objects.filter(user_id=user_id)            
            total_sold = sum(bookstore.total_sold for bookstore in bookstores)
            total_available = sum(bookstore.total_available for bookstore in bookstores)
            total_earnings = sum(bookstore.total_earnings for bookstore in bookstores)

            total_profit = total_earnings  

            data = {
                "total_sold": total_sold,
                "total_available": total_available,
                "total_earnings": total_earnings,
                "total_profit": total_profit
            }

            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            search_query = request.GET.get('query')
            if search_query:
                books = Bookstore.objects.filter(
                    user=user_id, title__icontains=search_query).order_by('-created_date')
            else:
                books = Bookstore.objects.filter(
                    user=user_id).order_by('-created_date')

            paginator = Paginator(books, 4)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            serializer = BooksSerializer(page_obj, many=True)
            return Response({
                'count': paginator.count,
                'num_pages': paginator.num_pages,
                'current_page': page_obj.number,
                'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
                'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
                'results': serializer.data
            })

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
