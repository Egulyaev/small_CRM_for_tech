from django import forms
from django.contrib.auth import get_user_model
from django.core.cache.utils import make_template_fragment_key
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Ticket

User = get_user_model()
POST_PER_PAGE = 5


class PagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='GulyaevEO')
        cls.ticket = Ticket.objects.create(
            ticket_text='Самый длинный тестовый пост',
            author=cls.user,
            type='service',
        )

        cls.all_urls = (
            (reverse('index'), 'tickets/index.html'),
            (reverse('new_ticket'), 'tickets/new.html',),
            (reverse('ticket_edit_staff',
                     kwargs={'ticket_id': cls.ticket.pk}),
             'tickets/edit_ticket_admin.html',),
            (reverse('ticket_view',
                     kwargs={'username': cls.user,
                             'ticket_id': cls.ticket.pk}),
             'tickets/ticket.html'),
            (reverse('ticket_edit',
                     kwargs={'username': cls.user,
                             'ticket_id': cls.ticket.pk}
                     ),
             'tickets/new.html',
             ),
            (reverse('all_tickets'), 'tickets/tickets_table.html',),
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PagesTests.user)

    def check_ticket_in_context_correct(self, ticket):
        ticket_author_1 = ticket.author
        post_text_1 = ticket.ticket_text
        self.assertEqual(ticket_author_1, PagesTests.user)
        self.assertEqual(post_text_1, PagesTests.ticket.ticket_text)

    def test_pages_use_correct_template(self):
        """URL-адреса используют соответствующий шаблон."""
        for adress, templates in PagesTests.all_urls:
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, templates)

    def test_index_shows_correct_context(self):
        """Шаблон index сформирован с правильным контекстом и
        созданный тикет появился на главной странице."""
        response = self.authorized_client.get(reverse('index'))
        first_object = response.context['page'][0]
        self.check_ticket_in_context_correct(first_object)

    def test_new_post_page_shows_correct_context(self):
        """Шаблон new_ticket  сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('new_ticket'))
        form_fields = {
            'type': forms.TypedChoiceField,
            'ticket_text': forms.CharField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_group_post_show_correct_context(self):
        """На главной странице отображается пост группы"""
        response = self.authorized_client.get(reverse('index'))
        first_object = response.context['page'][0]
        self.check_ticket_in_context_correct(first_object)

    def test_post_edit_correct_context(self):
        """Страница редактирования тикета
        сформирована с правильным контекстом"""
        response = self.authorized_client.get(
            reverse('ticket_edit',
                    kwargs={'username': PagesTests.user,
                            'ticket_id': PagesTests.ticket.pk, }
                    )
        )
        form_fields = {
            'type': forms.TypedChoiceField,
            'ticket_text': forms.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_page_correct_context(self):
        """Шаблон для страницы отдельного
        тикета сформирован с правильным контекстом"""
        response = self.authorized_client.get(
            reverse('ticket_view', kwargs={'username': PagesTests.user,
                                           'ticket_id': PagesTests.ticket.pk, })
        )
        self.assertEqual(response.context['author'].username,
                         PagesTests.user.username)
        self.assertEqual(response.context['ticket'].ticket_text,
                         PagesTests.ticket.ticket_text)

    def test_cache_page(self):
        key = make_template_fragment_key('index_page')
        self.assertIsNotNone(key)


class PaginationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='GulyaevEO')
        cls.ticket = Ticket.objects.create(
            ticket_text='Самый длинный тестовый пост',
            author=cls.user,
        )

        for i in range(11):
            Ticket.objects.create(
                ticket_text=f'Самый длинный тестовый пост{i}',
                author=cls.user,
            )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PaginationTests.user)

    def test_username_page_correct_context(self):
        """Шаблон для index сформирован с
        правильным контекстом и пагинатор работает корректно."""
        response = self.authorized_client.get(reverse('index'))
        self.assertEqual(response.context['ticket'].ticket_text, str(PaginationTests.ticket))
        self.assertEqual(len(response.context['page']), POST_PER_PAGE)
