from django.contrib import admin
from .models import Property, Category, Amenity, PropertyImage, Favorite

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'is_main', 'uploaded_at')

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'price', 'is_active')
    list_filter = ('is_active', 'category')
    search_fields = ('title', 'address')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'property', 'added_at')
