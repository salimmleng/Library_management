from django.contrib import admin
from django.urls import path
from .import views
urlpatterns = [
    path('',views.home, name= 'home'),
    path('category<slug:category_slug>/',views.home, name= 'category_wise_book'),
    path('book/<int:book_id>/', views.BookDetailView.as_view(), name='book_detail'),

    path('book_detail/<int:book_id>/',views.BookDetailView.as_view(), name = 'book_detail'),
    path('book_borrow/<int:borrow_book_id>/',views.BorrowBook.as_view(), name = 'borrow_book'),
    path('book_review/<int:review_book_id>/',views.AddReviewView.as_view(), name = 'add_review'),
    path('profile/',views.user_profile,name='profile'),
    path('return_book/<int:borrowed_book_id>/',views.return_book, name='return_book'),
]
