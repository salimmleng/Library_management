from django.db import models
from django.contrib.auth.models import User
from users.models import UserBankAccount

# Create your models here.



class Book_category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,blank=True,unique=True)

    def __str__(self):
        return f'{self.name}'
    

class Book(models.Model):
    img = models.ImageField(upload_to="books/media/uploads/")
    title = models.CharField(max_length=100)
    description = models.TextField()
    borrowing_price = models.IntegerField()
    category = models.ForeignKey(Book_category,on_delete=models.CASCADE)
   



    def __str__(self):
        return f'{self.title}'
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
   

class BorrowedBook(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    balance_after_borrowing = models.DecimalField(max_digits=10, decimal_places=2)
    borrowing_date = models.DateTimeField(auto_now_add=True)
    is_returned = models.BooleanField(default=False)

    


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.book.title}"


