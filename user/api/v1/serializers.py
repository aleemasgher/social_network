from django.http import HttpRequest
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from allauth.account.adapter import get_adapter
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    # name = serializers.CharField(required=False)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True, allow_blank=False)

    class Meta:
        model = User
        fields = ("id", 'username', "email", "first_name", 'last_name', "password")
        extra_kwargs = {
            "username": {
                "required": True,
                "allow_blank": False,
            },

        }

    def _get_request(self):
        request = self.context.get("request")
        if (
                request
                and not isinstance(request, HttpRequest)
                and hasattr(request, "_request")
        ):
            request = request._request
        return request

    def validate_password(self, password):
        if len(password) < 8 or password.lower() == password or password.upper() == password or password.isalnum() \
                or not any(i.isdigit() for i in password):
            raise serializers.ValidationError(
                    _("your password is too weak")
                )
        return password

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address.")
                )
        return email

    def create(self, validated_data):
        user = User(
            email=validated_data.get("email"),
            username=validated_data.get("username"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            name=validated_data.get("first_name")
        )
        user.set_password(validated_data.get("password"))
        user.save()
        return user

    def save(self, request=None):
        """rest_auth passes request so we must override to accept it"""
        return super().save()
