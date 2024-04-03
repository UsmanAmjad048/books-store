from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import ObtainAuthToken
urlpatterns = [
    path('books/', views.books, name='books'),
    path('search-books/', views.SearchBooksAPIView , name='search_books'),
    path('books/<int:user_id>/<int:book_id>/', views.booksuserid, name='booksid'),
    path('add-books/', views.AddBooksView.as_view(), name='add_books'),
    path('getuserbooks/<int:user_id>/', views.AddBooksView.as_view(), name='get_user_books'),
    path('getuserbooksid/<int:user_id>/<int:book_id>/', views.AddBooksView.as_view(), name='get_user_book_by_id'),
]
