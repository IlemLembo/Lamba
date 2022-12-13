from django.contrib import admin
from .models import User #, Profile

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display= ('username',"email", 'last_login', 'date_joined', 'phone')

'''
class ProfileAdmin(admin.ModelAdmin):
    list_display= ('user','pseudo','date_created', 'phone')
'''

admin.site.register(User, UserAdmin)


#admin.site.register(Profile, ProfileAdmin)