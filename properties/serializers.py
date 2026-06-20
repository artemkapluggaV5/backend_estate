from rest_framework import serializers
from properties.models import Category, Amenity, Property, PropertyImage, Favorite
from users.serializers import UserSerializer, AgentSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image_path', 'is_main', 'uploaded_at']

class PropertySerializer(serializers.ModelSerializer):
    photos = PropertyImageSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    category_details = CategorySerializer(source='category', read_only=True)
    agent_details = AgentSerializer(source='agent', read_only=True)
    agent = serializers.PrimaryKeyRelatedField(read_only=True)
    is_booked = serializers.SerializerMethodField()
    has_user_requested = serializers.SerializerMethodField()

    def get_is_booked(self, obj):
        return obj.viewing_requests.filter(payments__is_paid=True).exists()

    def get_has_user_requested(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.viewing_requests.filter(user=request.user).exists()
        return False

    class Meta:
        model = Property
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    property_details = PropertySerializer(source='property', read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Favorite
        fields = '__all__'