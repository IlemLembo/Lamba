from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# Create your models here.

class User(AbstractUser):
    # Let create Choices related variables :
    CREATOR = 'CREATOR'
    SUBSCRIBER = 'SUBSCRIBER'
    M = 'M'
    F = 'F'

    ROLES_CHOICES = (
        (CREATOR, "Créateur"),
        (SUBSCRIBER, "Abonné"),
    )

    GENDER_CHOICES = (
        (M, 'Masculin'),
        (F, 'Feminin'),
    )
    
    role = models.CharField(max_length=30, choices=ROLES_CHOICES, verbose_name='Rôle', null=True, blank=True )
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
    lastname = models.CharField(max_length=30, null=True, blank=True)
    firstname = models.CharField(max_length=100, null=True, blank=True)
    profile_photo = models.ImageField(verbose_name='Photo de Profil', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    bio = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=30 ,verbose_name = 'Numero de Telephone', null=True, blank=True)
    
    def __str__(self):
        return str(self.username)



'''
class Profile(models.Model):
    HOMME = 'Homme'
    FEMME = 'Femme'
    GENDER_CHOICES = (
        (HOMME, 'homme'),
        (FEMME, 'femme'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    lastname = models.CharField(max_length=30)
    firstname = models.CharField(max_length=50)
    pseudo = models.CharField(max_length=50, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    bio = models.TextField()
    phone = models.CharField(max_length=30 ,verbose_name = 'Numero de Telephone')
    def __str__(self):
        return str(self.user)
'''





'''
class Music(models.Model):
    likes = models.ManyToManyField(User, related_name='likes')
    def __str__(self):
        return self.likes.count()'''