from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Ticket, User


class TicketFormUser(ModelForm):
    class Meta:
        model = Ticket
        fields = ('type', 'ticket_text')
        help_texts = {
            'group': _('Тип запроса: ремонт, обслуживание, консультация'),
            'ticket_text': _('Описание запроса'),
        }


class TicketFormStaff(ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('id', 'date_joined', 'username', 'email', 'last_name', 'first_name', 'role',)