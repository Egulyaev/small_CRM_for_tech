from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TicketViewSet

router = DefaultRouter()
router.register('tickets', TicketViewSet, basename='api_tickets')
urlpatterns = [
    path('', include(router.urls)),
]