from rest_framework import viewsets, permissions
from rest_framework.response import Response
from . import models, serializers


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TicketSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Ticket.objects.all()
