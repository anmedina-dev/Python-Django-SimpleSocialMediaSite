from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

#UserCreaionForm only has username and password, so we created a new form to add the email
#Register User Form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField() 
    
    class Meta:
        model = User 
        fields = ['username', 'email', 'password1', 'password2']

#update user form
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField() 
    
    class Meta:
        model = User 
        fields = ['username', 'email']

#Udpate profile form
class ProfileUpdateForm(forms.ModelForm):
    class Meta: 
        model = Profile
        fields = ['image']