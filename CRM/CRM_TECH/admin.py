from django.contrib import admin

from .models import Ticket, User


class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'status', 'type', 'author',
        'worker', 'ticket_text', 'created', 'deadline',
    )
    search_fields = ('author',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_joined', 'username', 'email', 'last_name', 'first_name', 'role', 'password', )
    empty_value_display = '-пусто-'

admin.site.register(User, UserAdmin)
admin.site.register(Ticket, TicketAdmin)
