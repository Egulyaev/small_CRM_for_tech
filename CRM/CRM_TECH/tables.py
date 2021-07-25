import django_tables2 as tables
from django.shortcuts import redirect

from .models import Ticket, User


class TicketTable(tables.Table):
    Edit = tables.TemplateColumn(
        "<a href='/tickets/{{record.id}}'>Редактировать</a>",
        verbose_name='Редактировать заявку'
    )

    class Meta:
        model = Ticket
        template_name = 'django_tables2/bootstrap.html'
        fields = (
            'id', 'status', 'type', 'author', 'worker',
            'ticket_text', 'created', 'deadline',
        )


class UserTable(tables.Table):
    Edit = tables.TemplateColumn(
        "<a href='/user/{{record.username}}'>Редактировать</a>",
        verbose_name='Редактировать пользователя'
    )

    class Meta:
        model = User
        template_name = 'django_tables2/bootstrap.html'
        fields = (
            'id', 'date_joined', 'username',
            'email', 'last_name', 'first_name', 'role',
        )
