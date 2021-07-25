from datetime import datetime

from rest_framework import serializers

from CRM_TECH.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    current_date=serializers.DateTimeField(default=datetime.now())

    class Meta:
        fields = '__all__'
        model = Ticket
