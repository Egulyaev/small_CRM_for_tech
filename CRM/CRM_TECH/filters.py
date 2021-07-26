import django_filters

from .models import Ticket, User


class TicketModelFilter(django_filters.FilterSet):
    author = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        field_name='author',
        label='Автор заявки'
    )
    status = django_filters.CharFilter(
        label='Статус', lookup_expr='icontains'
    )
    type = django_filters.CharFilter(
        lookup_expr='iexact',
        label='Тип заявки'
    )
    created = django_filters.DateFromToRangeFilter(label='Период создания')

    class Meta:
        model = Ticket
        fields = ('author', 'status', 'type', 'created')
