from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + "\n" + self.description

class Samochody(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    marka = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    rok_produkcji = models.IntegerField()
    nr_rejestracyjny = models.CharField(max_length=20)
    pojemność_silnika = models.IntegerField()

class Przebiegi(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.DateField()
    przebieg = models.IntegerField()
    samochod = models.ForeignKey(Samochody, on_delete=models.CASCADE)

class Naprawy(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.DateField()
    opis = models.TextField()
    koszt = models.DecimalField(max_digits=10, decimal_places=2)
    samochod = models.ForeignKey(Samochody, on_delete=models.CASCADE)

class Tankowania(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.DateField()
    przebieg = models.IntegerField()
    ilość_paliwa = models.DecimalField(max_digits=6, decimal_places=2)
    cena_za_litr = models.DecimalField(max_digits=4, decimal_places=2)
    samochod = models.ForeignKey(Samochody, on_delete=models.CASCADE)

class Wydatki(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.DateField()
    opis = models.TextField()
    koszt = models.DecimalField(max_digits=10, decimal_places=2)
    samochod = models.ForeignKey(Samochody, on_delete=models.CASCADE)


