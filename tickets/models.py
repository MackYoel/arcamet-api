import os
import uuid
from decimal import Decimal

from django.db.models import F, Sum
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


def item_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4(), ext)
    return os.path.join('items/image', filename)


class ContactAbstract(models.Model):
    DNI = 1
    RUC = 2

    TYPE_CHOICES = (
        (DNI, 'DNI'),
        (RUC, 'RUC')
    )

    name = models.CharField(max_length=254)
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, default=DNI)
    document_number = models.CharField(max_length=11)
    phone = models.CharField(max_length=20)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Contact(ContactAbstract):
    pass


class Client(ContactAbstract):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)


class Ticket(models.Model):
    QUEUED = 1
    FINISHED = 2
    DELIVERED = 3

    STATES = (
        (QUEUED, 'En cola'),
        (FINISHED, 'Terminado'),
        (DELIVERED, 'Entregado'),
    )

    status = models.PositiveSmallIntegerField(choices=STATES, default=QUEUED)
    document_number = models.IntegerField()
    issue_date = models.DateTimeField(default=timezone.now, blank=True)
    delivery_date = models.DateTimeField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.document_number)

    @staticmethod
    def get_total_expression():
        subtotal = F('items__quantity') * F('items__unit_price')
        return Sum(subtotal)

    def save(self, *args, **kwargs):
        if self.id is None:
            self.document_number = type(self).objects.count() + 1
        super().save(*args, **kwargs)


class TicketItem(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=254)
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))])
    unit_price = models.DecimalField(
        max_digits=19,
        decimal_places=10,
        validators=[MinValueValidator(Decimal('0.00'))])
    image = models.ImageField(upload_to=item_image_path, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
