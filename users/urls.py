from django.contrib import admin
from django.urls import path
from .import views 
urlpatterns = [
    path('signup/',views.UserSignupView.as_view(), name = 'signup'),
    path('login/',views.UserLoginView.as_view(), name = 'login'),
    path('logout/',views.UserLogoutView.as_view(), name = 'logout'),
    path("deposit/", views.DepositMoneyView.as_view(), name="deposit_money"),
    

]
