from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ticket(models.Model):
    OPEN = 'open'
    IN_WORK = 'in_work'
    PENDING = 'pending'
    DONE = 'done'

    REPAIR = 'repair'
    SERVICE = 'service'
    CONSULTATION = 'consultation'

    STATUS_CHOICES = (
        (OPEN, 'Создан'),
        (IN_WORK, 'В работе'),
        (PENDING, 'Приостановлен'),
        (DONE, 'Выполнено')
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
        verbose_name="Пользователь"
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
