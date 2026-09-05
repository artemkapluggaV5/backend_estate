from django.db import models
from users.models import CustomUser, Agent

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Удобство")

    class Meta:
        verbose_name = "Удобство"
        verbose_name_plural = "Удобства"

    def __str__(self):
        return self.name

class Property(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, verbose_name="Риелтор")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Цена")
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Площадь")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    amenities = models.ManyToManyField(Amenity, blank=True, verbose_name="Удобства")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Объект недвижимости"
        verbose_name_plural = "Объекты недвижимости"

    def __str__(self):
        return self.title

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='photos', on_delete=models.CASCADE, verbose_name="Объект")
    image_path = models.CharField(max_length=500, verbose_name="Путь к изображению")
    is_main = models.BooleanField(default=False, verbose_name="Главное фото")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")

    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"

class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites', verbose_name="Пользователь")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorited_by', verbose_name="Объект")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        unique_together = ('user', 'property')