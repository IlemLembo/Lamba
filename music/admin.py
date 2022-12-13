from django.contrib import admin
from .models import *


class Music_Admin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'image', 'audio_file', 'price']

class Suggestion_Admin(admin.ModelAdmin):
    list_display = ['customer', 'content', 'date_created']

# Register your models here.
admin.site.register(Music, Music_Admin)
admin.site.register(Album)
admin.site.register(Order)
admin.site.register(Suggestion, Suggestion_Admin)

