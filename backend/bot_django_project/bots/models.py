from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


User = get_user_model()

# Вот он класс Bot, он эквивалентен таблице Bot в БД.
# В нем определены поля: name, token, description и т.д.
# В полях определены типы данных, и прочие параметры.
# В классе Meta определена сортировка по умолчанию, по id.
# В методе __str__ определено строковое представление объекта Bot.
# Идем обратно в сериалайзер.


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
        return f'Bot: {self.name}, Owner: {self.owner.username}'


class Message(models.Model):
    text = models.CharField(max_length=200)
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
    coordinate_x = models.SmallIntegerField(
        'Координата по оси x',
        validators=[
            MinValueValidator(0),
        ]
    )
    coordinate_y = models.SmallIntegerField(
        'Координата по оси y',
        validators=[
            MinValueValidator(0),
        ]
    )

    def __str__(self):
        return f'Message_id {self.id}: {self.text} of {self.bot}'


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

    def __str__(self):
        return f'Variant_id {self.id}: {self.text} to {self.current_message}'
