from rest_framework import viewsets

from CRM_TECH.models import Ticket
from api.serializers import TicketSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.filter()
    serializer_class = TicketSerializer
