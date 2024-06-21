from django.shortcuts import render,redirect
from .forms import RegistrationForm,DepositForm
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import DetailView
from django.urls import reverse_lazy
from .models import Transaction,UserBankAccount
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


# Create your views here.
class UserSignupView(CreateView):
    form_class = RegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self,form):
        messages.success(self.request,'Account created successfully')
        return super().form_valid(form)
    
    def form_invalid(self,form):
        messages.success(self.request,'Information incorrect')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Register'
        return context



class UserLoginView(LoginView):
    template_name = 'users/register.html'
    

    def form_valid(self,form):
        messages.success(self.request,'Logged in successful')
        return super().form_valid(form)

    def form_invalid(self,form):
        messages.success(self.request,'Login information incorrect')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context
    
    def get_success_url(self):
        return reverse_lazy('home')


class UserLogoutView(LoginRequiredMixin,LogoutView):
    def get_success_url(self):
        return reverse_lazy('home')
    






class TransactionCreateMixin(LoginRequiredMixin,CreateView):
    template_name = 'users/transaction_form.html'
    model = Transaction
    success_url = reverse_lazy('deposit_money')
    title = ''

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user_account,created = UserBankAccount.objects.get_or_create(user=self.request.user)
        kwargs.update({
            'account': user_account,
        })
        return kwargs
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,

        })
        return context
    




def send_transaction_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposite Form'

    
    def form_valid(self,form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount
        account.save(
            update_fields = [
                'balance',
            ]
        )
        
        messages.success(

            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )
        send_transaction_email(self.request.user, amount, "Deposite Message", "users/deposite_email.html")
        return super().form_valid(form)



