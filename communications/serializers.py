from rest_framework import serializers
from communications.models import ChatMessage, Review, Notification
from users.serializers import UserSerializer

class ChatMessageSerializer(serializers.ModelSerializer):
    sender_details = UserSerializer(source='sender', read_only=True)
    recipient_details = UserSerializer(source='recipient', read_only=True)
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ChatMessage
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
