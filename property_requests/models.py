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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='viewing_requests', verbose_name="Пользователь")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='viewing_requests', verbose_name="Объект недвижимости")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    scheduled_time = models.DateTimeField(null=True, blank=True, verbose_name="Назначенное время")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий клиента")

    class Meta:
        verbose_name = "Заявка на просмотр"
        verbose_name_plural = "Заявки на просмотр"

    def __str__(self):
        return f"Заявка #{self.id} от {self.user.username} на {self.property.title}"

class Payment(models.Model):
    request = models.ForeignKey(ViewingRequest, on_delete=models.CASCADE, related_name='payments', verbose_name="Заявка")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма платежа")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата платежа")
    is_paid = models.BooleanField(default=False, verbose_name="Статус оплаты")
    yookassa_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="ID платежа ЮKassa")

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"Платеж {self.amount} для заявки #{self.request.id}"
