from django.db import models
from users.models import CustomUser
from properties.models import Property

class ViewingRequest(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новая'),
        ('scheduled', 'Назначен просмотр'),
        ('completed', 'Завершена'),
        ('canceled', 'Отменена'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='viewing_requests', verbose_name="Пользователь", null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name="Имя", blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True, null=True)
    email = models.EmailField(verbose_name="Email", blank=True, null=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='viewing_requests', verbose_name="Объект недвижимости")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    scheduled_time = models.DateTimeField(null=True, blank=True, verbose_name="Запланированное время")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий клиента")

    class Meta:
        verbose_name = "Заявка на просмотр"
        verbose_name_plural = "Заявки на просмотры"

    def __str__(self):
        username = self.user.username if self.user else self.name
        return f"Заявка #{self.id} от {username} на {self.property.title}"

class CallRequest(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новая'),
        ('processed', 'Обработана'),
    )
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    time_to_call = models.CharField(max_length=100, blank=True, null=True, verbose_name="Время звонка")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Заказ звонка"
        verbose_name_plural = "Заказы звонков"

    def __str__(self):
        return f"Звонок для {self.name} ({self.phone})"

class ContactRequest(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новая'),
        ('processed', 'Обработана'),
    )
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True, null=True)
    message = models.TextField(verbose_name="Сообщение", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Сообщение из формы контактов"
        verbose_name_plural = "Сообщения из формы контактов"

    def __str__(self):
        return f"Сообщение от {self.name} ({self.email})"
