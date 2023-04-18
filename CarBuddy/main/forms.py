from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post
from .models import Samochody
from .models import Tankowania
from django.utils import timezone
from django.forms.widgets import NumberInput


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
class TankowanieForm(forms.ModelForm):
    ostatni_przebieg = forms.IntegerField(widget=NumberInput(attrs={'readonly': 'readonly'}), required=False)

    class Meta:
        model = Tankowania
        fields = ['samochod', 'data', 'przebieg', 'ilość_paliwa', 'cena_za_litr']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['samochod'].queryset = Samochody.objects.filter(author=user)
        self.fields['data'].widget.attrs['value'] = timezone.now().strftime('%Y-%m-%d')
        if 'instance' in kwargs:
            samochod = kwargs['instance'].samochod
            ostatnie_tankowanie = Tankowania.objects.filter(samochod=samochod).order_by('-data').first()
            if ostatnie_tankowanie:
                self.fields['ostatni_przebieg'].initial = ostatnie_tankowanie.przebieg

    def clean_przebieg(self):
        przebieg = self.cleaned_data['przebieg']
        ostatni_przebieg = self.cleaned_data['ostatni_przebieg']
        if ostatni_przebieg and przebieg < ostatni_przebieg:
            raise forms.ValidationError("Przebieg nie może być mniejszy niż ostatni przebieg: {}".format(ostatni_przebieg))
        return przebieg