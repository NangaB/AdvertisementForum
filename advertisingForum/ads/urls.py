from django.urls import path
from .import views

app_name = 'ads'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('register', views.register, name = 'register'),
    path('log', views.log, name = 'log'),
    path('logout', views.logoutuser, name = 'logout'),
    path('create', views.create, name = 'create'),
]