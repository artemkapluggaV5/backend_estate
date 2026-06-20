from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from property_requests.models import ViewingRequest, Payment
from communications.models import Notification
from property_requests.serializers import ViewingRequestSerializer, PaymentSerializer
from rest_framework.permissions import IsAuthenticated
import uuid
from yookassa import Configuration, Payment as YooKassaPayment
from django.conf import settings

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

class ViewingRequestViewSet(viewsets.ModelViewSet):
    serializer_class = ViewingRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        old_status = instance.status
        updated_instance = serializer.save()
        
        if old_status != updated_instance.status:
            status_map = {
                'scheduled': 'назначен',
                'completed': 'завершен',
                'canceled': 'отменен'
            }
            status_ru = status_map.get(updated_instance.status, updated_instance.status)
            Notification.objects.create(
                user=updated_instance.user,
                title='Обновление статуса заявки',
                content=f'Статус вашей заявки на объект "{updated_instance.property.title}" изменен на: {status_ru}.'
            )

    def get_queryset(self):
        user = self.request.user
        if user.role == 'client':
            return ViewingRequest.objects.filter(user=user)
        elif user.role == 'realtor':
            # Assuming agent is linked via agent profile, wait, property__agent is Agent model now
            return ViewingRequest.objects.filter(property__agent__user=user)
        elif user.role == 'admin':
            return ViewingRequest.objects.all()
        return ViewingRequest.objects.none()

    @action(detail=True, methods=['post'])
    def create_payment(self, request, pk=None):
        viewing_request = self.get_object()
        
        if viewing_request.status != 'completed':
            return Response({'error': 'Можно оплатить только завершенную заявку'}, status=status.HTTP_400_BAD_REQUEST)
            
        if Payment.objects.filter(request=viewing_request, is_paid=True).exists():
            return Response({'error': 'Объект уже оплачен'}, status=status.HTTP_400_BAD_REQUEST)
            
        amount = viewing_request.property.price
        
        payment = Payment.objects.create(
            request=viewing_request,
            amount=amount,
            is_paid=False
        )
        
        idempotence_key = str(uuid.uuid4())
        
        # В тестовой среде ЮKassa большие суммы (миллионы) сразу блокируются.
        # Поэтому для тестирования отправляем условные 100 рублей.
        test_amount = "100.00"
        
        res = YooKassaPayment.create({
            "amount": {
                "value": test_amount,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": f"http://localhost:5173/dashboard?verify_payment={payment.id}"
            },
            "capture": True,
            "description": f"Оплата объекта {viewing_request.property.title}"
        }, idempotence_key)
        
        payment.yookassa_id = res.id
        payment.save()
        
        return Response({'confirmation_url': res.confirmation.confirmation_url})

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        payment = self.get_object()
        
        if payment.is_paid:
            return Response({'status': 'success', 'message': 'Уже оплачено'})
            
        if not payment.yookassa_id:
            return Response({'error': 'Нет ID платежа ЮKassa'}, status=status.HTTP_400_BAD_REQUEST)
            
        yoo_payment = YooKassaPayment.find_one(payment.yookassa_id)
        
        if yoo_payment.status == 'succeeded':
            payment.is_paid = True
            payment.save()
            return Response({'status': 'success'})
            
        return Response({'status': yoo_payment.status})
