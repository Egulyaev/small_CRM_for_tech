from django.contrib.auth import get_user_model
from django.test import TestCase

from CRM_TECH.models import Ticket

User = get_user_model()


class TicketModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ticket = Ticket.objects.create(
            ticket_text='Самый длинный тестовый пост',
            author=User.objects.create_user(username='GulyaevEO'),
            type='service'
        )

    def test_str(self):
        """__str__  совпадает с ожидаемым."""
        ticket = TicketModelTest.ticket
        expected_text = ticket.ticket_text[:100]
        self.assertEquals(expected_text, str(ticket))
