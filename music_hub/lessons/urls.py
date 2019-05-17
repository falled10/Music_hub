from rest_framework.routers import DefaultRouter

from .views import LessonsViewSet

router = DefaultRouter()
router.register('lessons', LessonsViewSet, base_name='lessons')

urlpatterns = [

] + router.urls
