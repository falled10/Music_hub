from rest_framework.routers import DefaultRouter

from .views import RequestsViewSet

router = DefaultRouter()
router.register('requests', RequestsViewSet, base_name='requests')

urlpatterns = [

] + router.urls
