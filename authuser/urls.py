from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from django.contrib.auth.views import LogoutView, PasswordResetView,  PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.loginpage,name='login'),
    path('logout/',views.logoutpage,name='logout'),
    path('register/',views.registerpage,name='register'),
    path('updateuser/<str:pk>/',views.updateuserpage,name='updateuser'),
    path('reset/',views.resetpassword,name='reset'),
    path('alluser/',views.alluser,name='alluser'),
    path('studentregister/',views.studentregister,name='studentregister'),

    # Forget Password
    path('password-reset/', PasswordResetView.as_view(template_name='authuser/password_reset.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='authuser/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='authuser/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='authuser/password_reset_complete.html'),name='password_reset_complete'),

]