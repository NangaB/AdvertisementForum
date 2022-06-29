from django.urls import path
from . import views

urlpatterns = [
    path('ads', views.ListCreateAds.as_view()),
    path('ads/<int:pk>', views.RetrieveUpdateDelete.as_view()),
    path('displayIndustry/<str:pk>', views.DisplayIndustry.as_view()),
]
