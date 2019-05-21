from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, viewsets
from rest_framework.permissions import IsAuthenticated

from .permissions import OnlySafeMethods
from .serializers import RegisterSerializer, UserSerializer


class UserViewSets(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,
                          OnlySafeMethods]


class RegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class UserAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
