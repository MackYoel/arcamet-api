import django_filters

from rest_framework import viewsets, permissions
from utils import pagination

from . import models, serializers


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TicketSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = (pagination.StandardResultsSetPagination)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = models.Ticket.objects.all()
    ordering = ('-pk',)
    filter_fields = {
        'document_number': ['icontains']
    }
