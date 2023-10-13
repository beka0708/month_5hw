from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from .models import ConfirmCode


class BaseValidateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_password(self, password):
        return password


class AuthorizationValidateSerializer(BaseValidateSerializer):
    pass


class RegistrationValidateSerializer(BaseValidateSerializer):
    is_active = serializers.BooleanField(required=False, default=False)

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('user already exists')


class ConfirmCodeValidateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)
    code = serializers.CharField(min_length=6, max_length=6)

    def validate_product_id(self, user_id):
        try:
            ConfirmCode.objects.get(id=user_id)
        except ConfirmCode.DoesNotExist:
            raise ValidationError(f'Director with id ({user_id}) not found')
        return user_id