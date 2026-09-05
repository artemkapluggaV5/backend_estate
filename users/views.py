from rest_framework import viewsets, status
from rest_framework.response import Response
from users.models import CustomUser
from users.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]  # Регистрация открыта для всех
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == 'admin':
            return CustomUser.objects.all()  # Админ видит всех
        elif user.is_authenticated:
            return CustomUser.objects.filter(id=user.id)  # Обычный пользователь — только себя
        return CustomUser.objects.none()

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        # Пользователь может редактировать только себя
        if request.user.id != obj.id and request.user.role != 'admin':
            return Response({'error': 'Вы можете редактировать только свой профиль'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.id != obj.id and request.user.role != 'admin':
            return Response({'error': 'Вы можете редактировать только свой профиль'}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Удалять пользователей может только админ
        if request.user.role != 'admin':
            return Response({'error': 'Только администратор может удалять пользователей'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

