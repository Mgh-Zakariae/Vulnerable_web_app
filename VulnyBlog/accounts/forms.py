from django import forms
from .models import User

class registerUser(forms.Form):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
        
class loginUser(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)