from datetime import date, timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_ROLE = 'user'
    MODERATOR_ROLE = 'moderator'
    ADMIN_ROLE = 'admin'

    ROLE_CHOICES = (
        (USER_ROLE, 'Пользователь'),
        (MODERATOR_ROLE, 'Модератор'),
        (ADMIN_ROLE, 'Администратор')
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER_ROLE,
        verbose_name='Роль'
    )
    post = models.TextField(
        blank=True,
        verbose_name='Должность'
    )


    class Meta:
        ordering = ['-username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == self.USER_ROLE

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR_ROLE

    @property
    def is_admin(self):
        return self.role == self.ADMIN_ROLE


class Ticket(models.Model):
    OPEN = 'Открыто'
    IN_WORK = 'В работе'
    PENDING = 'Ожидание'
    DONE = 'Закрыто'

    REPAIR = 'Ремонт'
    SERVICE = 'Обслуживание'
    CONSULTATION = 'Консультация'

    STATUS_CHOICES = (
        (OPEN, 'Открыто'),
        (IN_WORK, 'В работе'),
        (PENDING, 'Ожидание'),
        (DONE, 'Закрыто')
    )

    TYPE_CHOICES = (
        (REPAIR, 'Ремонт'),
        (SERVICE, 'Обслуживание'),
        (CONSULTATION, 'Консультация')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user",
        verbose_name="Пользователь",
        null=True,
    )
    worker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="worker",
        verbose_name="Работник",
        blank=True,
        null=True,
    )

    ticket_text = models.TextField(verbose_name="Описание заявки")
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания заявки"
    )
    updated = models.DateTimeField(auto_now=True)
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default=OPEN,
        verbose_name="Тип заявки"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=OPEN,
        verbose_name="Статус",
    )
    deadline = models.DateTimeField(
        default=(date.today() + timedelta(7)),
        verbose_name="Дедлайн"
    )

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return self.ticket_text[:100]
