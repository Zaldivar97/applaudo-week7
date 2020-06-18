import datetime
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()
expire_delta = api_settings.JWT_REFRESH_EXPIRATION_DELTA
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_payload_encoder = api_settings.JWT_ENCODE_HANDLER


class RegisterUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    expires = serializers.SerializerMethodField(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'token',
            'expires',
            'message'
        )

    def get_message(self, obj):
        return 'Thank you for registering'

    def get_expires(self, obj):
        return timezone.now() + expire_delta - datetime.timedelta(seconds=100)

    def get_token(self, obj):
        user = obj
        payload = jwt_payload_handler(user)
        token = jwt_payload_encoder(payload)
        return token

    def validate_username(self, value):
        user_exists = User.objects.filter(username__iexact=value).exists()
        if user_exists:
            raise serializers.ValidationError('Username is not available')
        return value

    def validate_email(self, value):
        user_exists = User.objects.filter(email__iexact=value).exists()
        if user_exists:
            raise serializers.ValidationError('This account already exists')
        return value

    def validate(self, data):
        password1 = data.get('password1')
        password2 = data.pop('password2')
        if password1 != password2:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        user: User = User(
            username=validated_data.get('username'),
            email=validated_data.get('email')
        )
        user.set_password(validated_data.get('password1'))
        user.save()
        return user
