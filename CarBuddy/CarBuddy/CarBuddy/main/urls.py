from django import urls
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('create-post', views.create_post, name='create_post'),
    path('dodaj_samochod', views.dodaj_samochod, name='dodaj_samochod'),
    path('dziennik',views.samochody_uzytkownika, name='dziennik'),
    path('ctcb',views.ctcb, name='ctcb'),
    path('usuwanie', views.usuwanie, name='usuwanie'),
]

