from django import urls
from django.urls import path
from . import views


urlpatterns = [
    path('', views.ctcb, name='home'),
    path('home', views.ctcb, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('dodaj_samochod', views.dodaj_samochod, name='dodaj_samochod'),
    path('dziennik',views.samochody_uzytkownika, name='dziennik'),
    path('ctcb',views.ctcb, name='ctcb'),
    #path('dodaj_tankowanie',views.dodaj_tankowanie, name='dodaj_tankowanie'),
    path('dodaj_tankowanie/<int:samochod_id>/', views.dodaj_tankowanie, name='dodaj_tankowanie'),
    path('dodaj_wydatki/<int:samochod_id>/', views.dodaj_wydatki, name='dodaj_wydatki'),
    path('usun_wydatek/<int:pk>/', views.usun_wydatek, name='usun_wydatek'),
]
