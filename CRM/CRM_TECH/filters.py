import django_filters

from .models import Ticket


class TicketModelFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr='iexact')
    type = django_filters.CharFilter(field_name='name',
                                     lookup_expr='icontains')

    class Meta:
        model = Ticket
        fields = '__all__'
