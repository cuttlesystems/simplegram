# Generated by Django 4.1.2 on 2022-11-25 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0004_alter_message_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='coordinate_x',
            field=models.IntegerField(verbose_name='Координата по оси x'),
        ),
        migrations.AlterField(
            model_name='message',
            name='coordinate_y',
            field=models.IntegerField(verbose_name='Координата по оси y'),
        ),
    ]