from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate
from .forms import AdForm
from django.contrib.auth.decorators import login_required
from .models import Advertisement

# Create your views here.

def home(request):
    ads = Advertisement.objects.all()
    return render(request, 'home.html', {'ads' : ads})

def register(request):
    if request.method == "GET":
        return render(request, 'register.html', {'form' : UserCreationForm()})
    else:
        if request.POST.get('password1') == request.POST.get('password2'):
            try:
                user = User.objects.create_user(username = request.POST.get('username'), password = request.POST.get('password1'))
            except IntegrityError:
                error = 'This username is already taken. Try using different one'
                return render(request, 'register.html', {'form' : UserCreationForm(), 'error' : error})
            else:
                user.save()
                return redirect('ads:home')
        else:
            error = 'Passeord did not match. Try again'
            return render(request, 'register.html', {'form' : UserCreationForm(), 'error' : error})

def log(request):
    if request.method == "GET":
        return render(request, 'log.html', {'form' : AuthenticationForm()})
    else:
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request,user)
            return redirect('ads:home')
        else:
            error = 'Username or password is wrong. Try again'
            return render(request, 'log.html', {'form' : AuthenticationForm(), 'error' : error})

@login_required
def logoutuser(request):
     logout(request)
     return render(request, 'home.html')

@login_required
def create(request):
    if request.method == "GET":
        return render(request, 'create.html', {'form' : AdForm()})
    else:
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit = False)
            ad.user = request.user
            ad.save()
            return redirect('ads:home')
        else:
            error = 'something went wrong. Try agian'
            return render(request, 'create.html', {'form' : AdForm(), 'error' :error})
