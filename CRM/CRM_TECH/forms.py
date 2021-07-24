from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from .models import Ticket


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ('type', 'ticket_text')
        help_texts = {
            'group': _('Тип запроса: ремонт, обслуживание, консультация'),
            'ticket_text': _('Описание запроса'),
        }


