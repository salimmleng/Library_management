from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserBankAccount(models.Model):
    user = models.OneToOneField(User,related_name='account', on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
   



class Transaction(models.Model):
    account = models.ForeignKey(UserBankAccount,on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2,max_digits=12)
    

