from rest_framework import serializers
from ads.models import Advertisement

class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'
        read_only_fields = ('id','user','likes')