from django.contrib.auth import get_user_model
from rest_framework import serializers

from bots.models import Message, Variant


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id',
            'text',
            'photo',
            'video',
            'file',
            'bot',
            'coordinate_x',
            'coordinate_y'
        )


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = (
            'id',
            'text',
            'current_message',
            'next_message'
        )
