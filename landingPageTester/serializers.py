from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

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

class ConfigureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigureDetails
        fields = '__all__'


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']