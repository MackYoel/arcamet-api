from rest_framework.routers import DefaultRouter
from django.urls import path

from . import views

app_name = 'tickets'
router = DefaultRouter()

router.register('tickets', views.TicketViewSet, base_name='api_ticket')
router.register('clients', views.ClientViewSet, base_name='api_client')
router.register('contacts', views.ContactViewSet, base_name='api_contanct')

urlpatterns = router.urls + [
]
