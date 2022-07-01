from rest_framework import serializers
from ads.models import Advertisement
from django.contrib.auth.models import User

class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'
        read_only_fields = ('id','user','likes')

class UserSerializer(serializers.ModelSerializer):
    ads = serializers.PrimaryKeyRelatedField(many=True, queryset=Advertisement.objects.all())
    class Meta:
        model = User
        fields = ('id','username','password','ads')

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    