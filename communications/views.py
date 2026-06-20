from rest_framework import viewsets
from communications.models import ChatMessage, Review, Notification
from communications.serializers import ChatMessageSerializer, ReviewSerializer, NotificationSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from property_requests.models import Payment

class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChatMessage.objects.filter(Q(sender=user) | Q(recipient=user))

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        property_obj = serializer.validated_data['property']
        
        # Check if user has paid for this property
        has_paid = Payment.objects.filter(request__user=user, request__property=property_obj, is_paid=True).exists()
        
        if not has_paid:
            raise ValidationError("Отзывы могут оставлять только клиенты, оплатившие объект.")
            
        serializer.save(user=user)

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
