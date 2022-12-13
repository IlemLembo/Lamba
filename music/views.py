from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import Music_Form, ProfileUpdateForm, SuggestionForm
from . import models
import requests
from webapp.settings import API_KEY, PAYGATE_URL
import json
from django.contrib import messages

# PAYGATE API call function:
def paygate(PAYGATE_URL, order_info):
    payment_status = ""
    data = json.dumps(order_info)
    response = requests.post(PAYGATE_URL, json=data, headers={
        'Content-type': 'application/json',
        'Accept': 'text/plain'
        })

    """
    0 : Transaction enregistrée avec succès
    2 : Jeton d’authentification invalide
    4 : Paramètres Invalides
    6 : Doublons détectées. Une transaction avec le même identifiant existe déja.
    """
    if response.status_code == 0:
        payment_status = 'successfull'
    elif response.status_code == 2:
        payment_status = 'review your auth token'
    elif response.status_code == 4:
        payment_status = 'Invalid data'
    elif response.status_code == 6:
        payment_status = 'order_id already exist'

    # Now, return me the interpretation of this WTF status_code 😪:
    return payment_status



# Create your views here.

def dashboard(request):
    user = request.user
    if user.is_authenticated:
        data = models.Music.objects.all()
        owned_music = models.Order.get_order_by_customer(customer_id=request.user).values_list("article", flat=True)

        return render(request, 'dashboard.html', context={
            'data' : data,
            'owned_music': owned_music,
            'user': request.user,
        })

    else:
        return redirect('login')

        
@login_required
def news(request):
    data = models.Music.objects.filter(creator=request.user)
    return render(request, 'news.html', context={
        'user' : request.user,
        'data' : data,
    })
    
@login_required
def Audio_Upload(request):
    form = Music_Form()
    if request.method == 'POST':
        form = Music_Form(request.POST, request.FILES)
        if form.is_valid():
            # Gardes moi ça au chaud ne sauvegarde pas encore dans ma base de donnée:
            audio = form.save(commit=False)
            """models.Music(
                title = form.cleaned_data['title'],
                creator = request.user,
                albums = form.cleaned_data('albums'),
                audio_file = form.cleaned_data('audio_file'),
                image = form.cleaned_data('image'),
                price = form.cleaned_data('price'),
                genre = form.cleaned_data('genre')
            )"""
            # Spécifions le créateur du fichier:
            audio.creator = request.user
            # Maintenant tu peux sauvegarder 👌
            audio.save()
            return redirect('home')
        else:
            messages.error(request, 'your form is invalid')
            form = Music_Form()
    return render(request, 'publicate.html', context={
        'form' : form,
        "Albums": models.Album.objects.all(),
    })

#@login_required
def update_profile(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    context = {}
    if request.method =='POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
    else:
        form = ProfileUpdateForm(
            initial={
                'email': user.email,
                'username': user.username,
            }
        )


    context = {
        'form': form
        }
    return render(request, 'profile.html', context)

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

def success_signup(request):
    user = request.user
    context = {
        'user': user,
    }
    template = render_to_string('success_signup_email.html', {'name':user.username})
    email = EmailMessage(
        'Nos Felicitations, vous êtes inscrit !' ,
        template ,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    email.fail_silently=False
    email.send()
    return render(request, 'success_signup_email.html', context)

@login_required
def Suggestion(request):
    form = SuggestionForm()
    context= {}

    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggest = form.save(commit=False)

            # Spécifions le nom du client :
            suggest.customer = request.user

            # Sauvegardons maintenant :
            suggest.save()
            return redirect('home')
    else:
        form = SuggestionForm()

    return render(request, 'suggest.html', context={
        'form' : form,
    })

def lecture(request, pk):
    audio = models.Music.objects.get(id=pk)
    context = {}
    if request.user.is_authenticated:
        return render(request, 'lecture.html', context = {
            'data' : audio,
        })
        

    else:
        return redirect('login')
        
    return render(request, 'lecture.html', context)

def payment(request, pk):

    '''
    auth_token	Jeton d’authentification de l’e-commerce (Clé API)	OUI
    phone_number	Numéro de téléphone mobile du Client	OUI
    amount	Montant de la transaction sans la devise (Devise par défaut: FCFA)	OUI
    description	Détails de la transaction	NON
    identifier	Identifiant interne de la transaction de l’e-commerce. Cet identifiant doit etre unique.	OUI
    network
    '''
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        amount = request.POST.get('amount')
        network = request.POST.get('network')

        order = models.Order(
            customer = request.user,
            phone_number = phone_number,
            amount = amount,
            network = network,
        )
        # here linking my order to the article to buy
        order.article.add(models.Music.objects.get(id=pk))
        order.save()

        order_info = {
            "auth_token" : API_KEY,
            'phone_number' : phone_number,
            "amount" : amount,
            "description" : "none",
            "identifier" : order.id,
            "network" : network,
        }

        response = paygate(PAYGATE_URL, order_info)

        if response == "successful":

            order.status = True

        else :
            messages.error(request, "Une erreur s'est produite...")
            


    return render(request, 'payment_form.html')