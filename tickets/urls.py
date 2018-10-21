from rest_framework.routers import DefaultRouter
from django.urls import path

from . import views

app_name = 'tickets'
router = DefaultRouter()

router.register('tickets', views.TicketViewSet, base_name='api_ticket')

urlpatterns = router.urls + [
]
