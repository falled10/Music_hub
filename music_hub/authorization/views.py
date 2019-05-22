from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import OnlySafeMethods
from .serializers import RegisterSerializer, UserSerializer


class VerifyView(APIView):

    def get(self, request, uuid, format=None):
        user = get_user_model().objects.filter(verification_uuid=uuid,
                                               is_verified=False)
        if user:
            user = user.first()
            user.is_verified = True
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(
            {'Url already used': 'User does not exist or is already verified'},
            status=status.HTTP_404_NOT_FOUND)


class VerifiedTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        user = get_user_model().objects.filter(email=request.data['email'])
        if user and user.first().is_verified:
            return super().post(request, *args, **kwargs)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


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
