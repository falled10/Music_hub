from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('users', views.UserViewSets, base_name='users')
app_name = 'authorization'

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(), name='auth-register'),
    path('auth/login/', views.VerifiedTokenObtainPairView.as_view(),
         name='auth-login'),
    path('verify/<str:uuid>/', views.VerifyView.as_view(), name='verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/user/', views.UserAPIView.as_view(), name='auth-user'),
    path('user/<int:id>/', include('subscribers.urls'))
] + router.urls
