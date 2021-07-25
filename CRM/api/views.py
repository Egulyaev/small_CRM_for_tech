from rest_framework import viewsets, mixins
from rest_framework.response import Response

from CRM_TECH.models import Ticket
from api.serializers import TicketSerializer


class ListViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass


class TicketViewSet(ListViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def list(self, request):
        queryset = Ticket.objects.filter(author=request.user)
        serializer = TicketSerializer(queryset, many=True)
        return Response(serializer.data)
