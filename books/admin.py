from django.contrib import admin
from .models import Book,Book_category,UserProfile,BorrowedBook,Review
# Register your models here.
admin.site.register(Book)
admin.site.register(Book_category)
admin.site.register(UserProfile)
admin.site.register(BorrowedBook)
admin.site.register(Review)


