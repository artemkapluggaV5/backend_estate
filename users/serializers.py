from rest_framework import serializers
from users.models import CustomUser, Agent

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'role', 'phone_number', 'first_name', 'last_name']
        read_only_fields = ['role']  # Роль нельзя менять через API

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if not password:
            raise serializers.ValidationError({'password': 'Пароль обязателен при регистрации.'})
        # Принудительно ставим роль "клиент" — админов создаём только через manage.py
        validated_data['role'] = 'client'
        validated_data.pop('is_staff', None)
        validated_data.pop('is_superuser', None)
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # Запрещаем менять роль, is_staff, is_superuser через API
        validated_data.pop('role', None)
        validated_data.pop('is_staff', None)
        validated_data.pop('is_superuser', None)
        # Если передан пароль — хешируем его
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class AgentSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Agent
        fields = '__all__'
