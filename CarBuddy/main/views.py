from django.shortcuts import get_object_or_404, render, redirect
from .forms import RegisterForm, PostForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from .models import Post, Samochody, Tankowania, Wydatki
from .forms import SamochodyForm
from .forms import TankowanieForm
from .forms import WydatkiForm
from django.shortcuts import render
from django.http import HttpResponse



@login_required(login_url="/login")
def home(request):
    posts = Post.objects.all()

    if request.method == "POST":
        post_id = request.POST.get("post-id")
        user_id = request.POST.get("user-id")

        if post_id:
            post = Post.objects.filter(id=post_id).first()
            if post and (post.author == request.user or request.user.has_perm("main.delete_post")):
                post.delete()
        elif user_id:
            user = User.objects.filter(id=user_id).first()
            if user and request.user.is_staff:
                try:
                    group = Group.objects.get(name='default')
                    group.user_set.remove(user)
                except:
                    pass

                try:
                    group = Group.objects.get(name='mod')
                    group.user_set.remove(user)
                except:
                    pass

    return render(request, 'main/home.html', {"posts": posts})


@login_required(login_url="/login")
@permission_required("main.add_post", login_url="/login", raise_exception=True)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/home")
    else:
        form = PostForm()

    return render(request, 'main/create_post.html', {"form": form})


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})

def dodaj_samochod(request):
    my_models = Samochody.objects.filter(author=request.user)
    if request.method == 'POST':
        form = SamochodyForm(request.POST)
        if form.is_valid():
            samochod = form.save(commit=False)
            samochod.author = request.user
            samochod.save()
            return redirect('dziennik')
        else:
            print(form.errors)
    else:
        form = SamochodyForm()
    return render(request, 'main/dodaj_samochod.html', {'form': form, 'my_models': my_models})

def dodaj_tankowanie(request, samochod_id):
    samochod = get_object_or_404(Samochody, id=samochod_id, author=request.user)
    ostatnie_tankowanie = Tankowania.objects.filter(samochod=samochod).order_by('-data').first()
    
    if request.method == 'POST':
        form = TankowanieForm(request.POST, user=request.user, initial={'samochod': samochod})
        if form.is_valid():
            tankowanie = form.save(commit=False)
            tankowanie.save()
            form = TankowanieForm(user=request.user, initial={'samochod': samochod})
            if ostatnie_tankowanie:
                form.initial = {'przebieg': ostatnie_tankowanie.przebieg,
                                'ilość_paliwa': ostatnie_tankowanie.ilość_paliwa,
                                'cena_za_litr': ostatnie_tankowanie.cena_za_litr,
                                'samochod': samochod}
            return render(request, 'main/dodaj_tankowanie.html', {'form': form, 'samochod': samochod})
        else:
            print(form.errors)
    else:
        form = TankowanieForm(user=request.user, initial={'samochod': samochod})
        if ostatnie_tankowanie:
            form.initial = {'przebieg': ostatnie_tankowanie.przebieg,
                            'ilość_paliwa': ostatnie_tankowanie.ilość_paliwa,
                            'cena_za_litr': ostatnie_tankowanie.cena_za_litr,
                            'samochod': samochod}
    return render(request, 'main/dodaj_tankowanie.html', {'form': form, 'samochod': samochod})



def samochody_uzytkownika(request):
    samochody = Samochody.objects.filter(author=request.user)
    wydatki = Wydatki.objects.filter(samochod__in=samochody)
    if request.method == 'POST':
        samochod_id = request.POST.get('samochod')
        if samochod_id:
            tankowania = Tankowania.objects.filter(samochod__id=samochod_id)
            wydatki = Wydatki.objects.filter(samochod__id=samochod_id)
        else:
            tankowania = Tankowania.objects.filter(samochod__id__in=samochody.values_list('id', flat=True))
            wydatki = Wydatki.objects.filter(samochod__id__in=samochody.values_list('id', flat=True))
    else:
        tankowania = Tankowania.objects.filter(samochod__in=samochody)
        wydatki = Wydatki.objects.filter(samochod__in=samochody)
    return render(request, 'main/dziennik.html', {'samochody': samochody, 'tankowania': tankowania, 'wydatki': wydatki})

def ctcb(request):
    return render(request, 'main/ctcb.html')

def dodaj_wydatki(request, samochod_id):
    samochod = get_object_or_404(Samochody, pk=samochod_id, author=request.user)
    if request.method == 'POST':
        form = WydatkiForm(request.POST, user=request.user, initial={'samochod': samochod})
        if form.is_valid():
            wydatek = form.save(commit=False)
            wydatek.samochod = samochod
            wydatek.save()
           # return redirect('dodaj_wydatki', samochod_id=samochod_id )
        return redirect('dziennik')
    else:
        form = WydatkiForm(user=request.user, initial={'samochod': samochod})
    return render(request, 'main/dodaj_wydatki.html', {'form': form, 'samochod': samochod})



def usun_wydatek(request, pk):
    wydatek = get_object_or_404(Wydatki, pk=pk)
    wydatek.delete()
    return redirect('dziennik')

def usun_tankowanie(request, pk):
    tankowanie = get_object_or_404(Tankowania, pk=pk)
    tankowanie.delete()
    return redirect('dziennik')


