from django.shortcuts import get_object_or_404, render, redirect
from .forms import RegisterForm, PostForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from .models import Post, Samochody
from .forms import SamochodyForm
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
            return redirect('dodaj_samochod')
        else:
            print(form.errors)
    else:
        form = SamochodyForm()
    return render(request, 'main/dodaj_samochod.html', {'form': form, 'my_models': my_models})


def samochody_uzytkownika(request):
    samochody = Samochody.objects.filter(author=request.user)
    return render(request, 'main/dziennik.html', {'samochody': samochody})

def ctcb(request):
    return render(request, 'main/ctcb.html')

def usuwanie(request, id):
   usuwanie = get_object_or_404(Samochody, id, author=request.user)
   usuwanie.delete()
   return render(request, 'main/dziennik.html', {'usuwanie': samochody_uzytkownika.samochody})


