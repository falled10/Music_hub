from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from .models import Requests
from .permissions import IsSenderOrRecipient
from .serializers import RequestsSerializer


class RequestsViewSet(ModelViewSet):
    serializer_class = RequestsSerializer
    queryset = Requests.objects.all()
    permission_classes = [permissions.IsAuthenticated,
                          IsSenderOrRecipient]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
