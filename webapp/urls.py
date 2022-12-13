"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from authentication.views import LoginPageView, portal, LogoutPageView , SignupPageView, about
import music.views as musicviews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    path('login', LoginPageView, name='login'),
    path('', portal, name='portal'),
    path('logout/', LogoutPageView, name='logout'),
    path('signup/', SignupPageView, name='signup'),
    re_path(f'^home', musicviews.dashboard, name='home'),
    path('news', musicviews.news, name='news'),
    path('about', about, name='about'),
    path('update_profile', musicviews.update_profile, name='update_profile'),
    path('player/<str:pk>', musicviews.lecture, name='player'),
    #path("payment/<str:pk>", musicviews.payment),
    # YOUR_PATH_HERE,
    path('upload', musicviews.Audio_Upload, name='Upload_Audiofile'),

    # automated email
    path('success_signup_email', musicviews.success_signup, name='success_signup_email'),
    path('suggestion', musicviews.Suggestion, name='suggest'),

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

    '''+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))'''

    """ + static(settings.ADMIN_MEDIA_PREFIX, document_root=settings.ADMIN_STATIC_ROOT)"""