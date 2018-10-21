from rest_framework import serializers

from . import models


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Ticket
        fields = (
            'id',
            'issue_date',
            'delivery_date',
            'client'
        )
