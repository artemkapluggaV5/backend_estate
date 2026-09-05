from django.contrib import admin
from .models import ViewingRequest, CallRequest, ContactRequest

@admin.register(ViewingRequest)
class ViewingRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'user', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'property__title')
    raw_id_fields = ('user', 'property')

@admin.register(CallRequest)
class CallRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'phone')

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'phone')
