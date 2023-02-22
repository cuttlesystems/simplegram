# Generated by Django 4.1.2 on 2023-02-16 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0017_bot_must_be_started'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='Bot description'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bot',
            name='error_message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='error_message_bot', to='bots.message'),
        ),
        migrations.AlterField(
            model_name='bot',
            name='start_message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='first_message_bot', to='bots.message'),
        ),
        migrations.AlterField(
            model_name='bot',
            name='token',
            field=models.CharField(blank=True, default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='message',
            name='variable',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
    ]
