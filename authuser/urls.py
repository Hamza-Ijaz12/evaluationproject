from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.loginpage,name='login'),
    path('logout/',views.logoutpage,name='logout'),
    path('register/',views.registerpage,name='register'),
    path('reset/',views.resetpassword,name='reset'),
]