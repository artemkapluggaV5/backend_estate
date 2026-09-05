from rest_framework import viewsets
from properties.models import Category, Amenity, Property, PropertyImage, Favorite
from users.models import Agent
from properties.serializers import CategorySerializer, AmenitySerializer, PropertySerializer, PropertyImageSerializer, FavoriteSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class AmenityViewSet(viewsets.ModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Property.objects.filter(is_active=True)
        
        # Возвращаем все активные объекты, фильтрация по статусу "куплено" будет визуально отображаться на карточках
        category = self.request.query_params.get('category')
        max_price = self.request.query_params.get('max_price')

        if category:
            queryset = queryset.filter(category__name__icontains=category)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset.distinct()

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated and user.role == 'realtor':
            agent = Agent.objects.filter(user=user).first()
            serializer.save(agent=agent)
        else:
            serializer.save()

class PropertyImageViewSet(viewsets.ModelViewSet):
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)