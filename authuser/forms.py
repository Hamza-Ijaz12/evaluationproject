from django.forms import ModelForm
from .models import *


class UserForm(ModelForm):
    class Meta:
        model=User
        fields=['username','email','address','phone_number']


