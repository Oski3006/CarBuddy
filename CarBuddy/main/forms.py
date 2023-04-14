from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post
from .models import Samochody
from .models import Tankowania


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description"]

class SamochodyForm(forms.ModelForm):
    class Meta:
        model = Samochody
        fields = ['marka', 'model', 'nr_rejestracyjny', 'pojemność_silnika', 'rok_produkcji']
        labels = {
            'marka': 'Marka',
            'model': 'Model',
            'nr_rejestracyjny': 'Numer rejestracyjny',
            'pojemność_silnika': 'Pojemność silnika',
            'rok_produkcji': 'Rok produkcji'
        }
class TankowanieForm(forms.ModelForm):
    class Meta:
        model = Tankowania
        fields = ['data', 'przebieg', 'ilość_paliwa','cena_za_litr','samochod']
        labels = {
            'data': 'Data',
            'przebieg': 'Przebieg',
            'ilość_paliwa': 'Ilość Paliwa',
            'cena_za_litr': 'Cena za litr',
            'samochod': 'Samochód'
        }
        