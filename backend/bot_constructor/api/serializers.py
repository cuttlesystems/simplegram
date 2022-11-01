from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from bots.models import Bot, Message, Variant


User = get_user_model()


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'first_name', 'last_name', 'username', 'email')


class BotSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Bot
        fields = (
            'id',
            'name',
            'token',
            'description',
            'owner',
            'start_message'
        )
    
    validators = [
            UniqueTogetherValidator(
                queryset=Bot.objects.all(),
                fields=('name', 'owner'),
                message='Вы уже создавали бота с таким именем.',
            )
        ]


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
    
    def validate(self, data):
        if data.get('current_message') == data.get('next_message'):
            raise serializers.ValidationError(
                'Циклическая связь.'
            )
        return data

    validators = [
            UniqueTogetherValidator(
                queryset=Variant.objects.all(),
                fields=('text', 'current_message'),
                message='Такой вариант для сообщения уже существует.',
            )
        ]
