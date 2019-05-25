from rest_framework import serializers

from authorization.serializers import UserSerializer
from .models import Subscribers


class GetSubscribersSerializer(serializers.ModelSerializer):
    subscriber_user = UserSerializer(source='subscriber', read_only=True)

    class Meta:
        model = Subscribers
        fields = ('subscriber_user', )


class CreateSubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscribers
        fields = ('subscriber', 'user')
