from django.contrib import admin

from .models import Ticket


class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'status', 'type', 'author',
        'worker', 'ticket_text', 'created', 'deadline',
    )
    search_fields = ('author',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'


admin.site.register(Ticket, TicketAdmin)
