from django.contrib import admin
from .models import ViewingRequest, Payment

@admin.register(ViewingRequest)
class ViewingRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'user', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'property__title')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'request', 'amount', 'payment_date', 'is_paid')
    list_filter = ('is_paid',)
