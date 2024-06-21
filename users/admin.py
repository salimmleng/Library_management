from django.contrib import admin
from .models import UserBankAccount,Transaction
# Register your models here.
admin.site.register(UserBankAccount)
admin.site.register(Transaction)