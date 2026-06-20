from rest_framework import serializers
from property_requests.models import ViewingRequest, Payment
from properties.serializers import PropertySerializer
from users.serializers import UserSerializer

class ViewingRequestSerializer(serializers.ModelSerializer):
    property_details = PropertySerializer(source='property', read_only=True)
    user_details = UserSerializer(source='user', read_only=True)
    is_paid = serializers.SerializerMethodField()

    class Meta:
        model = ViewingRequest
        fields = '__all__'
        read_only_fields = ['user']

    def get_is_paid(self, obj):
        return obj.payments.filter(is_paid=True).exists()

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
