from rest_framework import viewsets
from communications.models import ChatMessage, Review, Notification, GuestChat, GuestMessage
from communications.serializers import ChatMessageSerializer, ReviewSerializer, NotificationSerializer, GuestChatSerializer, GuestMessageSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.exceptions import ValidationError

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
        if user.role == 'realtor':
            raise ValidationError("Риелторы не могут оставлять отзывы о компании.")
        serializer.save(user=user)

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class GuestChatViewSet(viewsets.ModelViewSet):
    serializer_class = GuestChatSerializer
    queryset = GuestChat.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'session_id'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return GuestChat.objects.all()
        session_id = self.request.query_params.get('session_id')
        if session_id:
            return GuestChat.objects.filter(session_id=session_id)
        return GuestChat.objects.none()

    @action(detail=False, methods=['post'])
    def start(self, request):
        session_id = request.data.get('session_id')
        if not session_id:
            return Response({'error': 'session_id is required'}, status=400)
        chat, created = GuestChat.objects.get_or_create(session_id=session_id)
        serializer = self.get_serializer(chat)
        return Response(serializer.data)


class GuestMessageViewSet(viewsets.ModelViewSet):
    serializer_class = GuestMessageSerializer
    queryset = GuestMessage.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        session_id = self.request.query_params.get('session_id')
        if session_id:
            return GuestMessage.objects.filter(chat__session_id=session_id)
        if self.request.user.is_authenticated:
            return GuestMessage.objects.all()
        return GuestMessage.objects.none()

    def perform_create(self, serializer):
        session_id = self.request.data.get('session_id')
        if not session_id:
            raise ValidationError("session_id is required")
        chat, _ = GuestChat.objects.get_or_create(session_id=session_id)
        sender = 'staff' if self.request.user.is_authenticated else 'client'
        serializer.save(chat=chat, sender=sender)
