from rest_framework import serializers
from users.models import CustomUser, Agent

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'role', 'phone_number', 'first_name', 'last_name']
        read_only_fields = ['role']  # Роль нельзя менять через API

    def validate_username(self, value):
        import re
        if len(value) < 4:
            raise serializers.ValidationError("Имя пользователя должно содержать не менее 4 символов.")
        if len(value) > 30:
            raise serializers.ValidationError("Имя пользователя не должно превышать 30 символов.")
        if not re.match(r"^[a-zA-Z0-9_]+$", value):
            raise serializers.ValidationError("Имя пользователя может содержать только латинские буквы, цифры и символ подчеркивания.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Пароль должен содержать не менее 8 символов.")
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value

    def validate_phone_number(self, value):
        import re
        if not value:
            return value
        if not re.match(r"^(\+7|8)\d{10}$", value):
            raise serializers.ValidationError("Введите корректный российский номер телефона (например, +79991234567 или 89991234567).")
        if CustomUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Пользователь с таким номером телефона уже существует.")
        return value

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
