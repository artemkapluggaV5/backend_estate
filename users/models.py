from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        return super().create_superuser(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Клиент'),
        ('realtor', 'Риелтор'),
        ('admin', 'Администратор'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client', verbose_name="Роль")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Agent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='agent_profile', verbose_name="Пользователь")
    experience_years = models.IntegerField(default=0, verbose_name="Стаж работы (лет)")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00, verbose_name="Рейтинг")

    class Meta:
        verbose_name = "Риелтор"
        verbose_name_plural = "Риелторы"

    def __str__(self):
        return f"Риелтор: {self.user.username}"
