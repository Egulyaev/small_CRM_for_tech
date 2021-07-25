from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from CRM_TECH.forms import TicketFormUser
from CRM_TECH.models import Ticket

User = get_user_model()


class TaskCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='GulyaevEO')
        cls.ticket = Ticket.objects.create(
            ticket_text='Самый длинный тестовый пост',
            author=cls.user,
            type='service'
        )
        cls.form = TicketFormUser()

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(TaskCreateFormTests.user)

    def test_create_ticket(self):
        """Валидная форма создает ticket."""
        ticket_count = Ticket.objects.count()
        form_data = {
            'type': 'service',
            'ticket_text': 'Самый длинный тестовый пост 2',
        }

        response = self.authorized_client.post(
            reverse('new_ticket'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(Ticket.objects.count(), ticket_count + 1)
        self.assertTrue(
            Ticket.objects.filter(
                ticket_text='Самый длинный тестовый пост 2',
            ).exists()
        )

    def test_edit_post(self):
        """При редактировании поста через форму на
        странице /<username>/<ticket_id>/edit/
        изменяется соответствующая запись в базе данных"""
        ticket_count = Ticket.objects.count()
        form_data = {
            'type': 'service',
            'ticket_text': 'Измененный текст',
        }

        response = self.authorized_client.post(
            reverse('ticket_edit',
                    kwargs={'username': TaskCreateFormTests.user,
                            'ticket_id': TaskCreateFormTests.ticket.id, }),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response,
                             reverse('ticket_view',
                                     kwargs={
                                         'username': TaskCreateFormTests.user,
                                         'ticket_id': self.ticket.id, }))
        self.assertEqual(Ticket.objects.count(), ticket_count)
        self.assertTrue(
            Ticket.objects.filter(
                ticket_text='Измененный текст',
                type='service'
            ).exists()
        )
