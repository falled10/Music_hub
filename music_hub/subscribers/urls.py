from django.urls import path

from .views import SubscriberViewSet

urlpatterns = [
    path('subscribers/', SubscriberViewSet.as_view({'get': 'list'}),
         name='subscribers'),
    path('subscribe/', SubscriberViewSet.as_view({'post': 'subscribe'}),
         name='subscribe'),
    path('unsubscribe/', SubscriberViewSet.as_view({'post': 'unsubscribe'}),
         name='unsubscribe')
]
