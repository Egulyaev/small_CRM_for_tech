from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from CRM_TECH.models import Ticket

User = get_user_model()


class RightURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='GulyaevEO')
        cls.user2 = User.objects.create_user(username='user')
        cls.ticket = Ticket.objects.create(
            ticket_text='Самый длинный тестовый пост',
            author=cls.user,
        )
        # cls.public_urls = (
        #     ('/', 'posts/index.html'),
        #     (f'/group/{cls.group.slug}/', 'posts/group.html'),
        #     (f'/{cls.user}/', 'posts/profile.html'),
        #     (f'/{cls.user}/{cls.post.pk}/', 'posts/post.html'),
        # )
        cls.private_urls = (
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
             'tickets/tickets_table.html'
             ),
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(RightURLTests.user)
        self.authorized_client2 = Client()
        self.authorized_client2.force_login(RightURLTests.user2)

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

    def test_private_auth_pages(self):
        """Приватные страницы имеют код 200
        при авторизованном клиенте"""
        for adress, _ in RightURLTests.private_urls:
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    # def test_authorized_edit_post_page(self):
    #     """Страница редактирования поста для
    #     авторизованного пользователя (НЕ автор) имеет код 302"""
    #     response = self.authorized_client2.get(
    #         f'/{RightURLTests.user}/{RightURLTests.post.pk}/edit/'
    #     )
    #     self.assertEqual(response.status_code, HTTPStatus.FOUND)
    #     self.assertRedirects(response,
    #                          reverse(
    #                              'post_view',
    #                              kwargs={'username': RightURLTests.user,
    #                                      'post_id': RightURLTests.post.pk})
    #                          )

    # def test_public_urls_uses_correct_template(self):
    #     """Все публичные страницы используют ожидаемый шаблон"""
    #     for adress, template in RightURLTests.public_urls:
    #         with self.subTest(adress=adress):
    #             response = self.authorized_client.get(adress)
    #             self.assertTemplateUsed(response, template)

    def test_private_urls_uses_correct_template(self):
        """Все приватные страницы используют ожидаемый шаблон"""
        for adress, template in RightURLTests.private_urls:
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)

    def test_404_page(self):
        """Проверка, что сервер возвращает 404 если страница не найдена"""
        response = self.authorized_client.get('/212345/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
