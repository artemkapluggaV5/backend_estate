from rest_framework import serializers
from property_requests.models import ViewingRequest, CallRequest, ContactRequest
from properties.serializers import PropertySerializer
from users.serializers import UserSerializer

class ViewingRequestSerializer(serializers.ModelSerializer):
    property_details = PropertySerializer(source='property', read_only=True)
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = ViewingRequest
        fields = '__all__'

class CallRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallRequest
        fields = '__all__'

        read_only_fields = ['user']

class ContactRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactRequest
        fields = '__all__'
