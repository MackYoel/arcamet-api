from rest_framework import serializers

from . import models


class ContactAbstractSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ContactAbstract
        fields = (
            'id',
            'name',
            'type',
            'get_type_display',
            'document_number',
            'phone'
        )


class ContactSerializer(ContactAbstractSerializer):
    class Meta:
        model = models.Contact
        fields = ContactAbstractSerializer.Meta.fields


class ClientSerializer(ContactAbstractSerializer):
    contact = ContactSerializer()

    class Meta:
        model = models.Client
        fields = ContactAbstractSerializer.Meta.fields + (
            'contact',
        )


class TicketItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TicketItem
        fields = ('description', 'quantity', 'unit_price', 'image')


class TicketSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Client.objects.all(),
        write_only=True,
        source='client')
    total = serializers.SerializerMethodField()
    items = TicketItemSerializer(many=True)
    user_display = serializers.SerializerMethodField()

    class Meta:
        model = models.Ticket
        fields = (
            'id',
            'document_number',
            'issue_date',
            'delivery_date',
            'client',
            'client_id',
            'total',
            'user_display',
            'status',
            'items',
        )
        extra_kwargs = {
            'document_number': {'read_only': True}
        }

    def get_total(self, obj):
        if hasattr(obj, 'total'):
            return obj.total
        return 0

    def get_user_display(self, obj):
        return obj.user.username

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        ticket = models.Ticket.objects.create(**validated_data)
        for item_data in items_data:
            item_data['id'] = None
            models.TicketItem.objects.create(ticket=ticket, **item_data)

        return ticket


class TicketListSerializer(serializers.ModelSerializer):
    client_display = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = models.Ticket
        fields = (
            'id',
            'document_number',
            'issue_date',
            'delivery_date',
            'client_display',
            'get_status_display',
            'total'
        )

    def get_total(self, obj):
        if hasattr(obj, 'total'):
            return obj.total
        return 0

    def get_client_display(self, obj):
        client = obj.client
        if client:
            return client.name
        return '-'
