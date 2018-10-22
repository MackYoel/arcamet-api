import django_filters

from rest_framework import filters, viewsets, permissions
from utils import pagination

from . import models, serializers


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TicketSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = (pagination.StandardResultsSetPagination)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter)
    ordering = ('-pk',)
    filter_fields = {
        'document_number': ['icontains']
    }

    def get_queryset(self):
        queryset = models.Ticket.objects
        if self.action == 'list':
            queryset = queryset.select_related(
                'client').annotate(total=models.Ticket.get_total_expression())
        else:
            queryset = queryset.select_related('user').prefetch_related(
                'client__contact', 'items').annotate(
                total=models.Ticket.get_total_expression())
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.TicketListSerializer
        return serializers.TicketSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ContactSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = (pagination.StandardResultsSetPagination)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    ordering = ('-pk',)
    filter_fields = {
        'name': ['icontains']
    }
    queryset = models.Contact.objects.all()


class ClientViewSet(ContactViewSet):
    serializer_class = serializers.ClientSerializer
    queryset = models.Client.objects.select_related('contact').all()
