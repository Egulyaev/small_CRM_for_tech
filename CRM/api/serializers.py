from rest_framework import serializers

from CRM_TECH.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ticket
