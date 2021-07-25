from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from CRM_TECH.models import Ticket

User = get_user_model()


class RightURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='admin', role='admin')
        cls.user2 = User.objects.create_user(username='moderator', role='moderator')
        cls.user3 = User.objects.create_user(username='user', role='user')
        cls.ticket = Ticket.objects.create(
            ticket_text='Самый длинный тестовый пост',
            author=cls.user,
        )
        cls.ticket2 = Ticket.objects.create(
            ticket_text='Самый длинный тестовый пост',
            author=cls.user2,
        )
        cls.ticket3 = Ticket.objects.create(
            ticket_text='Самый длинный тестовый пост',
            author=cls.user3,
        )

        cls.private_urls_admin = (
            ('/',
             'tickets/index.html'
             ),
            ('/new/',
             'tickets/new.html'
             ),
            (f'/tickets/{cls.ticket.pk}/',
             'tickets/edit_ticket_admin.html'
             ),
            (f'/{cls.user}/{cls.ticket.pk}/',
             'tickets/ticket.html'
             ),
            (f'/{cls.user}/{cls.ticket.pk}/edit/',
             'tickets/new.html'
             ),
            ('/alltickets/',
             'tickets/table.html'
             ),
            (f'/user/{cls.user}/',
             'tickets/new.html'
             ),
            ('/allusers/',
             'tickets/table.html'
             ),
        )

        cls.private_urls_moderator = (
            ('/',
             'tickets/index.html'
             ),
            ('/new/',
             'tickets/new.html'
             ),
            (f'/tickets/{cls.ticket2.pk}/',
             'tickets/edit_ticket_admin.html'
             ),
            (f'/{cls.user2}/{cls.ticket2.pk}/',
             'tickets/ticket.html'
             ),
            (f'/{cls.user2}/{cls.ticket2.pk}/edit/',
             'tickets/new.html'
             ),
            ('/alltickets/',
             'tickets/table.html'
             ),
        )

        cls.private_urls_user = (
            ('/',
             'tickets/index.html'
             ),
            ('/new/',
             'tickets/new.html'
             ),

            (f'/{cls.user3}/{cls.ticket3.pk}/',
             'tickets/ticket.html'
             ),
            (f'/{cls.user3}/{cls.ticket3.pk}/edit/',
             'tickets/new.html'
             ),
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(RightURLTests.user)
        self.authorized_client2 = Client()
        self.authorized_client2.force_login(RightURLTests.user2)
        self.authorized_client3 = Client()
        self.authorized_client3.force_login(RightURLTests.user3)

    # def test_public_pages(self):
    #     """Публичные страницы имеют код ответа 200"""
    #     for adress, _ in RightURLTests.public_urls:
    #         with self.subTest(adress=adress):
    #             response = self.guest_client.get(adress)
    #             self.assertEqual(response.status_code, HTTPStatus.OK)

    # def test_private_pages(self):
    #     """Приватные страницы имеют рабочий редирект
    #     при гостевом клиенте"""
    #     for adress, _ in RightURLTests.private_urls:
    #         with self.subTest(adress=adress):
    #             response = self.guest_client.get(adress)
    #             self.assertEqual(response.status_code, HTTPStatus.FOUND)
    #             self.assertRedirects(response, f'/auth/login/?next={adress}')

    def test_private_auth_pages_admin(self):
        """Приватные страницы имеют код 200
        при авторизованном клиенте c ролью администратор"""
        for adress, _ in RightURLTests.private_urls_admin:
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_private_auth_pages_moderator(self):
        """Приватные страницы имеют код 200
        при авторизованном клиенте c ролью модератор"""
        for adress, _ in RightURLTests.private_urls_moderator:
            with self.subTest(adress=adress):
                response = self.authorized_client2.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_private_auth_pages_user(self):
        """Приватные страницы имеют код 200
        при авторизованном клиенте c ролью user"""
        for adress, _ in RightURLTests.private_urls_user:
            with self.subTest(adress=adress):
                response = self.authorized_client3.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_authorized_edit_ticket_page(self):
        """Страница редактирования тикета для
        авторизованного пользователя (НЕ автор) имеет код 302"""
        response = self.authorized_client3.get(
            f'/{RightURLTests.user}/{RightURLTests.ticket.pk}/edit/'
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response,
                             reverse(
                                 'ticket_view',
                                 kwargs={'username': RightURLTests.user,
                                         'ticket_id': RightURLTests.ticket.pk})
                            )

    def test_private_urls_uses_correct_template(self):
        """Все приватные страницы используют ожидаемый шаблон"""
        for adress, template in RightURLTests.private_urls_admin:
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)

    def test_404_page(self):
        """Проверка, что сервер возвращает 404 если страница не найдена"""
        response = self.authorized_client.get('/212345/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
