from rest_framework import serializers
from .models import *

class landingPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields='__all__'