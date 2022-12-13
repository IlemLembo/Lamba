from django import forms
from .models import Music, Album, Suggestion
from authentication.models import User

class Music_Form(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['title', 'albums', 'image', 'audio_file', 'genre', 'price']

    title = forms.CharField(max_length=60)
    image = forms.ImageField()
    albums = forms.ModelChoiceField(
        queryset=Album.objects.all(),
        required=False
    )

class Album_Form(forms.ModelForm):
    class Meta:
        model = Album
        fields=['title', 'Author', 'image', 'description', 'musics']


'''
class ContactUsForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField(widget=forms.EmailInput)
    message = forms.CharField(max_length=1000)'''


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'lastname', 'firstname', 'email',  'profile_photo', 'gender', 'bio', 'phone')

class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ('customer', 'content')

    content = forms.CharField(widget=forms.TextInput, min_length=50, max_length=4000)

