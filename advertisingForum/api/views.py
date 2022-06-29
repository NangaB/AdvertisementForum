from django.shortcuts import render
from rest_framework.views import APIView
from ads.models import Advertisement
from .serializer import AdSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from django.http.response import Http404

class ListCreateAds(APIView):
    def get(self, request):
        ads = Advertisement.objects.all()
        serializer = AdSerializer(ads, many = True)
        return Response(data=serializer.data)

    def post(self, request):
        serializer = AdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=User.objects.get(is_staff=True))
            #na razie każde ogłoszenie przypisane adminowi(is_staff=True)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            # return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetrieveUpdateDelete(APIView):
    def get_object(self, pk):
        #obslugujemy stan gdy nie ma takiego okłoszenie w bazie
        try:
            return Advertisement.objects.get(pk=pk)
        except Advertisement.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        ad = self.get_object(pk)
        serializer = AdSerializer(instance=ad)
        return Response(data=serializer.data)

    def put(self, request, pk):
        ad = self.get_object(pk)
        serializer = AdSerializer(instance=ad, data=request.data)
        if serializer.is_valid(): #musimy podać wszystkie dane żeby to przeszło
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ad = self.get_object(pk)
        ad.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DisplayIndustry(APIView):
    def get(self, request, pk):
        try:
            ads = Advertisement.objects.filter(industry=pk)
            if ads.count() != 0:
                serializer = AdSerializer(instance=ads, many=True)
                return Response(data=serializer.data)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        except ads.DoesNotExist:
            raise Http404








