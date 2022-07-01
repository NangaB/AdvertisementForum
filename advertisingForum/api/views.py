from urllib import request
from django.shortcuts import render
from rest_framework.views import APIView
from ads.models import Advertisement
from .serializer import AdSerializer, UserSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from django.http.response import Http404
from rest_framework.permissions import AllowAny, IsAuthenticated


class ListCreateAds(APIView):
    def get(self, request):
        ads = Advertisement.objects.all()
        serializer = AdSerializer(ads, many = True)
        return Response(data=serializer.data)

    def post(self, request):
        serializer = AdSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save(user=User.objects.get(is_staff=True))
            #wyżej to każde ogłoszenie przypisane adminowi(is_staff=True)
            serializer.save(user=request.user)
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

    def is_owner(self, request, object):
        return request.user == object.user

    def get(self, request, pk):
        ad = self.get_object(pk)
        serializer = AdSerializer(instance=ad)
        return Response(data=serializer.data)

    def put(self, request, pk):
        ad = self.get_object(pk)
        if self.is_owner(request,ad):
            serializer = AdSerializer(instance=ad, data=request.data)
            if serializer.is_valid(): #musimy podać wszystkie dane żeby to przeszło
                serializer.save()
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'response':"You don't have permission to edit this object"})

    def delete(self, request, pk):
        ad = self.get_object(pk)
        if self.is_owner(request,ad):
            ad.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'response':"You don't have permission to delete this object"})
    
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
            raise 
        
class ListCreateUser(APIView):
    def get(self, request):
        if request.user.is_staff:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        else:
            return Response({'response': "You do not have permission to get this data"})

    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUser(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.data)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListMyAds(APIView):
    def get(self, request):
        ads = Advertisement.objects.filter(user_id=request.user)
        serializer = AdSerializer(instance=ads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class Likes(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            ad = Advertisement.objects.get(pk=pk)
        except Advertisement.DoesNotExists():
            raise Http404
        
        if ad.likes.filter(id=request.user.id).exists():
            ad.likes.remove(request.user)
            return Response({'action':"Disliked"})
        else:
            ad.likes.add(request.user)
            return Response({'action':"Liked"})




