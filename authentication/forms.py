from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.fields import EmailField
from django.forms.forms import Form
from .models import User
  





class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label='Nom d`Utilisateur', widget=forms.TextInput, required=True)
    password = forms.CharField(max_length=63, label='Mot de Passe', widget=forms.PasswordInput, required=True)


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='username', min_length=5, max_length=150, help_text='min=5 max= 150')
    email = forms.EmailField(label='email', widget=forms.EmailInput)  
    password1 = forms.CharField(label='password', widget= forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget= forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def username_clean(self):
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("Nom d'utilisateur déja pris")  
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError("Cet Email existe déja")  
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Les mots de passe doivent être identiques")  
        return password2  
  
    def save(self, commit=True):  
        user = User.objects.create_user(
            self.cleaned_data['username'],  
            self.cleaned_data['email'],  
            self.cleaned_data['password1']
        )  
        return user

class User_Form(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput, label="email")

    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError("Cet Email existe déja")  
        return email 


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

