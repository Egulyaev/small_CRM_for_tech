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
        (OPEN, 'open'),
        (IN_WORK, 'in_work'),
        (PENDING, 'pending'),
        (DONE, 'done')
    )

    TYPE_CHOICES = (
        (REPAIR, 'repair'),
        (SERVICE, 'service'),
        (CONSULTATION, 'consultation')
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

    ticket_text = models.TextField()
    created = models.DateTimeField(auto_now=True)
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default=OPEN
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=OPEN,
    )
    deadline = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return self.ticket_text[:100]