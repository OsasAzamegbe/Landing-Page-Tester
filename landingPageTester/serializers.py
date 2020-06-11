from rest_framework import serializers
from .models import *

class TrafficSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields='__all__'

class SpeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speed
        fields = '__all__'

class CountSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkCount
        fields = '__all__'