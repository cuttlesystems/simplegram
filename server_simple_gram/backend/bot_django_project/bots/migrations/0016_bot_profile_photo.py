# Generated by Django 4.1.2 on 2023-02-03 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0015_merge_20230119_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='bot_profile_images/'),
        ),
    ]