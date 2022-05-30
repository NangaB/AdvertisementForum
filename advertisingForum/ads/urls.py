from django.urls import path
from django.views import View
from .import views

app_name = 'ads'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('register', views.register, name = 'register'),
    path('log', views.log, name = 'log'),
    path('logout', views.logoutuser, name = 'logout'),
    path('create', views.create, name = 'create'),
    path('<int:adId>', views.detail, name = 'detail'),
    path('my', views.my, name = 'my'),
    path('my/<int:adId>', views.edit, name = 'edit'),
    path('delete/<int:adId>', views.deleteAd, name = 'delete'),
    path('search', views.search, name = 'search'),
    path('industry/<str:industryKey>', views.displayIndustry, name = 'display_industry'),
]