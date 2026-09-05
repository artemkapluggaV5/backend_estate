from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Сначала пытаемся найти пользователя по email
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                # Если не нашли, пытаемся найти по username
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        except User.MultipleObjectsReturned:
            user = User.objects.filter(email=username).first()

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
