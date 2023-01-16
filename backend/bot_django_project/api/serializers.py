from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from bots.models import Bot, Message, Variant, Command

User = get_user_model()


class BotSerializer(serializers.ModelSerializer):
    """
    Вот он BotSerializer, в кратце зачем он нужен:

    В нашем примере поступает GET запрос, то есть запрос на получение каких-то данных.
    Сериалайзер связан с таблицей из БД, а именно с таблицей Bot.
    Таблица Bot содержит столбцы (поля), которые мы определили в файле models.py для класса Bot.
    Переместитесь в файл models.py, посмотреть на class Bot и возвращайтесь обратно.

    Так вот сериалайзер получит данные из таблицы, превратит их в JSON, который мы вернем в API ответе
    Тут в классе мета в переменной fields определены поля, которые и будут в API ответе
    Данными можно манипулировать, можно добавить свое поле не из БД, или результат каких-то вычислений.
    Возвращайтесь во views.py
    """
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
            'keyboard_type',
            'photo',
            'video',
            'file',
            'bot',
            'coordinate_x',
            'coordinate_y',
            'message_type',
            'next_message'
        )
        read_only_fields = ('bot',)


class VariantSerializer(serializers.ModelSerializer):
    current_message = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=None
    )

    class Meta:
        model = Variant
        fields = (
            'id',
            'text',
            'current_message',
            'next_message'
        )

    validators = [
            UniqueTogetherValidator(
                queryset=Variant.objects.all(),
                fields=('text', 'current_message'),
                message='This variant is alredy exists.',
            )
        ]


class MessageSerializerWithVariants(serializers.ModelSerializer):
    current_variants = VariantSerializer(
        many=True,
        read_only=True)

    next_variants = VariantSerializer(
        many=True,
        read_only=True)

    class Meta:
        model = Message
        fields = (
            'id',
            'text',
            'keyboard_type',
            'photo',
            'video',
            'file',
            'bot',
            'coordinate_x',
            'coordinate_y',
            'current_variants',
            'next_variants'
        )
        read_only_fields = ('bot', 'current_variants', 'next_variants')


class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = (
            'id',
            'bot',
            'command',
            'description'
        )
        read_only_fields = ('bot',)
