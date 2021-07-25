import django_tables2 as tables

from .models import Ticket


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
