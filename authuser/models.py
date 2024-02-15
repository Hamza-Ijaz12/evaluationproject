from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .manager import CustomUserManager
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from django.contrib.auth.tokens import default_token_generator


# Create your models here.

# Models start here

def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/profiles/user_<id>/<filename>
    return f"profiles/user_{instance.id}/{filename}"

class User(AbstractBaseUser,PermissionsMixin):
    # basic information
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255,blank=True)
    address = models.CharField(max_length=255,blank=True)
    phone_number = models.CharField(max_length=255,blank=True,default='')
    # profile image
    avatar = models.ImageField(null=True,default='profile/avatar.png',upload_to=user_directory_path)

    #Choices
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ) 
    #role assiging
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default='student')
    

    # permissions
    is_active =models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # record
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # First login check for teacher
    first_login = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        app_label = 'authuser'

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username or self.email  

    def get_short_name(self):
        return self.username or self.email.split('@')[0]
    
# @receiver(post_save,sender=User)
# def print_password(sender,instance,email,**kwargs):
#     if email != '':
#         print('===========',yourpassword)
