from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        verification_code = uuid.uuid4()

        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.verification_code = verification_code
        user.save()

        verification_link = f"{settings.SITE_URL}{reverse('email-verify', args=[user.verification_code])}"

        send_mail(
            'Подтверждение почты',
            f'Пожалуйста, подтвердите вашу почту, перейдя по следующей ссылке: {verification_link}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return user
