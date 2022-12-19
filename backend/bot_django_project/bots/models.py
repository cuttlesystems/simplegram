from django.db import models
from django.contrib.auth import get_user_model

from utils.cut_string import cut_string
from b_logic.data_objects import ButtonTypes

MAX_CHARS = 50

User = get_user_model()

# Вот он класс Bot, он эквивалентен таблице Bot в БД.
# В нем определены поля: name, token, description и т.д.
# В полях определены типы данных, и прочие параметры.
# В классе Meta определена сортировка по умолчанию, по id.
# В методе __str__ определено строковое представление объекта Bot.
# Идем обратно в сериалайзер.


KEYBOARD_TYPES = [
    (ButtonTypes.REPLY.value, 'Reply Keyboard'),
    (ButtonTypes.INLINE.value, 'Inline Keyboard'),
]


class Bot(models.Model):
    name = models.CharField(max_length=200)
    token = models.CharField(max_length=100, null=True)
    description = models.TextField('Описание бота', null=True)
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
        'Координата по оси x'
    )
    coordinate_y = models.IntegerField(
        'Координата по оси y'
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        string = f'Message_id {self.id}: {self.text}'
        return cut_string(string, MAX_CHARS)


class Variant(models.Model):
    text = models.CharField(max_length=200)
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
