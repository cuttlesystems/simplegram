from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


User = get_user_model()


class Bot(models.Model):
    name = models.CharField(max_length=200)
    token = models.CharField(max_length=100)
    description = models.TextField('Описание бота')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bots'
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Message(models.Model):
    text = models.CharField(max_lenth=200)
    photo = models.ImageField(
        upload_to='messages/',
        null=True,
        blank=True
    )
    # video = 
    # file = 
    bot = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    coordinate_x = models.SmallIntegerField(
        'Координата по оси x',
        validators=[
            MinValueValidator(1),
        ]
    )
    coordinate_y = models.SmallIntegerField(
        'Координата по оси y',
        validators=[
            MinValueValidator(1),
        ]
    )


class Variant(models.Model):
    text = models.CharField(max_lenth=200)
    current_message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='current_variants'
    )
    next_message = models.ForeignKey(
        Message,
        on_delete=models.SET_NULL,
        related_name='next_variants'
    )
