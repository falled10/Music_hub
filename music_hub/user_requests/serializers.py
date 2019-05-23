from rest_framework import serializers

from .models import Requests


class RequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
        fields = ('title', 'body', 'sender', 'recipient')
