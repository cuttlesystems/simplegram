from django.db import models
from django.contrib.auth import get_user_model

from common_utils.cut_string import cut_string
from b_logic.data_objects import ButtonTypesEnum, MessageTypeEnum

User = get_user_model()

# Вот он класс Bot, он эквивалентен таблице Bot в БД.
# В нем определены поля: name, token, description и т.д.
# В полях определены типы данных, и прочие параметры.
# В классе Meta определена сортировка по умолчанию, по id.
# В методе __str__ определено строковое представление объекта Bot.
# Идем обратно в сериалайзер.
MAX_CHARS = 50

_MAX_COMMAND_LENGTH = 32
_MAX_COMMAND_DESCRIPTION_LENGTH = 256

KEYBOARD_TYPES = [
    (ButtonTypesEnum.REPLY.value, 'Reply Keyboard'),
    (ButtonTypesEnum.INLINE.value, 'Inline Keyboard'),
]


class MessageTypesDjango(models.TextChoices):
    VARIANTS = MessageTypeEnum.VARIANTS.value
    ANY_INPUT = MessageTypeEnum.ANY_INPUT.value
    GOTO = MessageTypeEnum.GOTO.value


class Bot(models.Model):
    name = models.CharField(max_length=200)
    token = models.CharField(max_length=100, null=True)
    description = models.TextField('Bot description', null=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bots'
    )
    start_message = models.ForeignKey(
        'Message',
        on_delete=models.SET_NULL,
        related_name='first_message_bot',
        null=True
    )
    error_message = models.ForeignKey(
        'Message',
        on_delete=models.SET_NULL,
        related_name='error_message_bot',
        null=True
    )
    profile_photo = models.ImageField(
        upload_to='bot_profile_images/',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        string = f'Bot {self.id}: {self.name}'
        return cut_string(string, MAX_CHARS)


class Message(models.Model):
    text = models.TextField()
    keyboard_type = models.CharField(
        max_length=3,
        choices=KEYBOARD_TYPES,
        default='RKB'
    )
    photo = models.ImageField(
        upload_to='messages_images/',
        null=True,
        blank=True
    )
    video = models.FileField(
        upload_to='messages_videos/',
        null=True,
        blank=True
    )
    file = models.FileField(
        upload_to='messages_files/',
        null=True,
        blank=True
    )
    bot = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    coordinate_x = models.IntegerField(
        'Coordinate by x axis'
    )
    coordinate_y = models.IntegerField(
        'Coordinate by y axis'
    )
    message_type = models.CharField(
        max_length=20,
        choices=MessageTypesDjango.choices,
        default=MessageTypesDjango.VARIANTS
    )
    next_message = models.ForeignKey(
        'Message',
        on_delete=models.SET_NULL,
        related_name='next_messages',
        null=True,
        blank=True
    )
    variable = models.TextField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        string = f'Message_id {self.id}: {self.text}'
        return cut_string(string, MAX_CHARS)


class Variant(models.Model):
    text = models.CharField(max_length=120)
    current_message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='current_variants'
    )
    next_message = models.ForeignKey(
        Message,
        on_delete=models.SET_NULL,
        related_name='next_variants',
        null=True,
        blank=True
    )

    def display_bot(self):
        """Метод для отображения бота для варианта в админке"""
        return f'{self.current_message.bot}'

    display_bot.short_description = 'Bot'

    class Meta:
        ordering = ['id']

    def __str__(self):
        string = f'Variant_id {self.id}: {self.text}'
        return cut_string(string, MAX_CHARS)


class Command(models.Model):
    bot = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE,
        related_name='commands'
    )
    command = models.CharField(max_length=_MAX_COMMAND_LENGTH)
    description = models.CharField(max_length=_MAX_COMMAND_DESCRIPTION_LENGTH)

    class Meta:
        ordering = ['id']

    def __str__(self):
        string = f'Command_id {self.id}: {self.command}'
        return cut_string(string, MAX_CHARS)


class StartedBotsStorage(models.Model):
    bots_list = models.TextField('Started bots')
    created_at = models.DateTimeField('Creation date', auto_now_add=True)

    class Meta:
        get_latest_by = ['created_at']
        verbose_name = 'Started bots storage'

    def __str__(self):
        string = f'Started bots: {self.bots_list}'
        return cut_string(string, MAX_CHARS)
