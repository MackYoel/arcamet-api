from django.contrib import admin
from . import models


class TicketItemInline(admin.TabularInline):
    model = models.TicketItem


@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('issue_date', 'delivery_date', 'client')
    inlines = [TicketItemInline]


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'document_number', 'phone', 'contact')


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'document_number', 'phone')
