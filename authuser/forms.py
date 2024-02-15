from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm



# class UserForm(ModelForm):
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

#     class Meta:
#         model=User
#         fields=['username','email','address','phone_number','passsword1','password2']


class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email','avatar', 'address', 'phone_number')

class UserupdateForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email','avatar', 'address', 'phone_number')

class StudentUserForm(forms.Form):
    csv_file = forms.FileField(
        label='Select a CSV file',
        help_text='Make sure the CSV file follows the correct format.'
    )
