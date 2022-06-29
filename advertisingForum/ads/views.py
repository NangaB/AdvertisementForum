from ast import keyword
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate
from .forms import AdForm
from django.contrib.auth.decorators import login_required
from .models import Advertisement
from django.db.models import Q

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
        return render(request, 'create.html', {'form' : AdForm(), 'ad' : Advertisement})
    else:
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit = False)
            ad.user = request.user
            ad.save()
            return redirect('ads:home')
        else:
            error = 'something went wrong. Try agian'
            return render(request, 'create.html', {'form' : AdForm(), 'error' :error, 'ad' : Advertisement})

def detail(request, adId):
    ad = get_object_or_404(Advertisement, pk=adId)
    if ad.likes.filter(id=request.user.id).exists():
        ad.is_liked = True
    else:
        ad.is_liked = False
    return render(request, 'detail.html', {'ad' : ad})


def my(request):
    ads = Advertisement.objects.filter(user=request.user)
    return render(request, 'my.html', {'ads' : ads})

@login_required
def edit(request, adId):
    ad = get_object_or_404(Advertisement, pk=adId, user = request.user)
    if request.method == "GET":
        form = AdForm(instance = ad)
        return render(request, 'edit.html', {'form' : form, 'ad' : ad})
    else:
        form = AdForm(request.POST, instance = ad)
        if form.is_valid():
            form.save()
            return redirect('ads:my')
        else:
            error = 'Something went wrong'
            return render(request, 'edit.html', {'form':form, 'ad' : ad, 'error' : error})

@login_required
def deleteAd(request, adId):
    ad = get_object_or_404(Advertisement, pk=adId, user = request.user)
    ad.delete()
    return redirect('ads:my')

def search(request):
    keyWords = request.POST.get('search').split(' ')
    for word in keyWords:
        querySet = Advertisement.objects.filter(Q(company__icontains=word) | Q(desc__icontains=word))
    try:
        ads = ads | querySet
    except:
        ads = querySet
    return render(request, 'home.html', {'ads' : ads})

def displayIndustry(request, industryKey):
    ads = Advertisement.objects.filter(industry = industryKey)
    return render(request, 'home.html', {'ads' : ads})

@login_required
def likes(request,adId):
    ad = get_object_or_404(Advertisement, pk = adId)
    if ad.likes.filter(id=request.user.id).exists():
        ad.likes.remove(request.user)
    else:
        ad.likes.add(request.user)
    return redirect('ads:detail', adId = ad.id)

