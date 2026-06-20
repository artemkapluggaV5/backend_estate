from django.db import models
from users.models import CustomUser
from properties.models import Property

class ChatMessage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages', verbose_name="Отправитель")
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages', verbose_name="Получатель")
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Объект (если связано)")
    message_text = models.TextField(verbose_name="Сообщение")
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")

    class Meta:
        verbose_name = "Сообщение чата"
        verbose_name_plural = "Сообщения чата"
        ordering = ['-sent_at']

    def __str__(self):
        return f"От {self.sender} к {self.recipient} ({self.sent_at})"

class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews', verbose_name="Пользователь")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews', verbose_name="Объект")
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Оценка")
    comment = models.TextField(blank=True, null=True, verbose_name="Текст отзыва")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.property.title}"

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications', verbose_name="Пользователь")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Системное уведомление"
        verbose_name_plural = "Системные уведомления"

    def __str__(self):
        return f"Уведомление для {self.user.username}: {self.title}"
