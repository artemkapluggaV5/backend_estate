from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from property_requests.models import ViewingRequest, CallRequest, ContactRequest
from communications.models import Notification
from property_requests.serializers import ViewingRequestSerializer, CallRequestSerializer, ContactRequestSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.mail import send_mail
from django.conf import settings

class ViewingRequestViewSet(viewsets.ModelViewSet):
    serializer_class = ViewingRequestSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()

    def perform_update(self, serializer):
        instance = self.get_object()
        old_status = instance.status
        updated_instance = serializer.save()
        
        if old_status != updated_instance.status:
            status_map = {
                'scheduled': 'Назначен просмотр',
                'completed': 'Завершен',
                'canceled': 'Отменен'
            }
            status_ru = status_map.get(updated_instance.status, updated_instance.status)
            Notification.objects.create(
                user=updated_instance.user,
                title='Статус заявки обновлен',
                content=f'Статус вашей заявки на объект "{updated_instance.property.title}" изменен на: {status_ru}.'
            )

    def get_queryset(self):
        user = self.request.user
        if user.role == 'client':
            return ViewingRequest.objects.filter(user=user)
        elif user.role == 'realtor':
            return ViewingRequest.objects.filter(property__agent__user=user)
        elif user.role == 'admin':
            return ViewingRequest.objects.all()
        return ViewingRequest.objects.none()

class CallRequestViewSet(viewsets.ModelViewSet):
    serializer_class = CallRequestSerializer
    queryset = CallRequest.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        instance = serializer.save()
        try:
            send_mail(
                'Новый заказ звонка на Юг-Хаус',
                f'Поступила новая заявка на звонок!\n\nИмя: {instance.name}\nТелефон: {instance.phone}\nВремя звонка: {instance.time_to_call or "Не указано"}',
                getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@yughouse.ru'),
                [getattr(settings, 'ADMIN_EMAIL', 'admin@yughouse.ru')],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Failed to send email: {e}")

class ContactRequestViewSet(viewsets.ModelViewSet):
    serializer_class = ContactRequestSerializer
    queryset = ContactRequest.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        instance = serializer.save()
        try:
            send_mail(
                'Новое сообщение из формы контактов на Юг-Хаус',
                f'Поступило новое сообщение!\n\nИмя: {instance.name}\nEmail: {instance.email}\nТелефон: {instance.phone or "Не указано"}\nСообщение: {instance.message or "Пусто"}',
                getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@yughouse.ru'),
                [getattr(settings, 'ADMIN_EMAIL', 'admin@yughouse.ru')],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Failed to send email: {e}")
