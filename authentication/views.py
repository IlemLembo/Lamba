from django.shortcuts import render, redirect
#from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import User_Form
from django.contrib.auth.forms import UserCreationForm
from music.views import *

# Create your views here.
def LoginPageView(request):
    template_name = 'authentication\login.html'
    message = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,
                username = username,
                password = password,
                )            
        if user is not None:
            login(request, user)
            return redirect('home')
            message = 'connected'
        else:
            messages.success(request, 'Identifiant invalides. Veuillez réessayer!')

            return redirect('login')
    else:
        return render(request, template_name,{})


def portal(request):
    data = models.Music.objects.all()
    return render(request, 'home/home.html',{
        'data' : data[0:4],
    })

def LogoutPageView(request):
    logout(request)

    messages.success(request, "Vous êtes déconnecté! ")
    return redirect('login')

def SignupPageView(request):
    if request.POST:
        form = User_Form(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            raw_password = form.cleaned_data['password1']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request,
                username = username,
                password = password,
            )
            login(request, user)
            success_signup(request)

            #messages.success(request, ('Vous êtes désormais inscrit!'))
            return redirect('home')
    else:
        form = User_Form()
    context = {
        'form' : form,
    }

    return render(request, 'registration/signup.html', context)

def about(request):
    return render(request, 'home/about.html')

