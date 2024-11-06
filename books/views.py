from django.shortcuts import render,redirect
from .models import Book_category,Book, Review,UserProfile,BorrowedBook
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import DetailView,View
from .forms import CommentForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from users.models import UserBankAccount
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.decorators import method_decorator
from .models import Book, UserProfile, BorrowedBook, Review, UserBankAccount



class BookDetailView(DetailView):

    model = Book
    pk_url_kwarg = 'book_id'
    template_name = 'books/book_details.html'
    context_object_name = 'book'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Review.objects.filter(book = self.object)
        context['comment_form'] = CommentForm()
        if self.request.user.is_authenticated:
            user_profile, created = UserProfile.objects.get_or_create(user=self.request.user)
            borrowed_book = BorrowedBook.objects.filter(user_profile=user_profile, book=self.object, is_returned=False).exists()
            context['has_borrowed'] = borrowed_book

        else:
            context['has_borrowed'] = False

        return context
    


    

class BorrowBook(View):
    
    def post(self,request,borrow_book_id):
        book = get_object_or_404(Book, id = borrow_book_id)
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
         
        try:
            user_account = UserBankAccount.objects.get(user=request.user)

        except UserBankAccount.DoesNotExist:
            messages.error(request, 'Your bank balance is totally 0, please deposite first')

            return redirect('book_detail',book_id=borrow_book_id)

        if user_account.balance >= book.borrowing_price:
            user_account.balance -= book.borrowing_price
            user_account.save()

            try:
                borrowed_book = BorrowedBook.objects.get(user_profile = user_profile,book = book)

            except BorrowedBook.DoesNotExist:
                borrowed_book = BorrowedBook(
                    user_profile = user_profile,
                    book = book,
                    balance_after_borrowing = user_account.balance

                )
                borrowed_book.save()

                messages.success(request, f"You have successfully borrowed '{book.title}'. Your account has been charged ${book.borrowing_price}.")

            send_transaction_email(request.user, user_account.balance, "BookBorrow Message", "books/book_borrow_email.html")

        else:
            messages.error(request, 'You do not have enough balance to borrow this book, please deposit first.')

        return redirect('book_detail', book_id=borrow_book_id)
        



class AddReviewView(View):
    def post(self, request, review_book_id):
        book = get_object_or_404(Book, id=review_book_id)
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)

        borrowed_book = BorrowedBook.objects.filter(user_profile=user_profile, book=book, is_returned=False).exists()
        
        if not borrowed_book:
            messages.error(request, 'You need to borrow the book to add a review.')
            return redirect('book_detail', book_id=review_book_id)

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.book = book
            comment.user_profile = user_profile
            comment.save()
            messages.success(request, 'Review added successfully.')

        return redirect('book_detail', book_id=review_book_id)



def send_transaction_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()





def home(request,category_slug = None):
    book = Book.objects.all()
    if category_slug is not None:
        category1 = Book_category.objects.get(slug = category_slug)
        book = Book.objects.filter(category = category1)

    category = Book_category.objects.all()

    return render(request,'books/home2.html',{'book': book, 'category': category})


@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    borrowed_books = BorrowedBook.objects.filter(user_profile=profile)
    
    return render(request, 'books/profile.html', {'borrowed_books': borrowed_books})




def return_book(request,borrowed_book_id):
    if request.method == 'POST':
        user_profile = get_object_or_404(UserProfile,user = request.user)
        borrowed_book = get_object_or_404(BorrowedBook,id = borrowed_book_id,user_profile = user_profile)
        # book instance
        book = borrowed_book.book
        borrowed_book.is_returned = True
        borrowed_book.save()

        # update user's balance
        user_account = get_object_or_404(UserBankAccount,user = request.user)
        user_account.balance += book.borrowing_price
        user_account.save()
        messages.success(request,f"You have successfully returned '{book.title}'. $'{book.borrowing_price}' has been credited back to you account.")
        return redirect('profile')
    else:
        messages.error(request,'Invalid request')
        return redirect('profile')
    

    




    