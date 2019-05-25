from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import Subscribers
from .serializers import CreateSubscribeSerializer, GetSubscribersSerializer


class SubscriberViewSet(ListModelMixin, ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = get_object_or_404(get_user_model(), id=self.kwargs['id'])
        serializer = GetSubscribersSerializer(user.followers.all(), many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def subscribe(self, request, id=None):
        if self.request.user.id == id:
            return Response('Can`t subscribe to yourself',
                            status=status.HTTP_400_BAD_REQUEST)
        data = {
            'user': id,
            'subscriber': self.request.user.id
        }
        serializer = CreateSubscribeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def unsubscribe(self, request, id=None):
        data = Subscribers.objects.filter(
            user=id,
            subscriber=self.request.user.id).exists()
        if data:
            subscription = Subscribers.objects.get(
                user=id,
                subscriber=self.request.user.id)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response('There is no subscription with this data',
                        status=status.HTTP_400_BAD_REQUEST)
