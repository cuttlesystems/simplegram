from django.contrib import admin

from .models import Bot, Message, Variant

admin.site.register(Bot)
admin.site.register(Message)
admin.site.register(Variant)
