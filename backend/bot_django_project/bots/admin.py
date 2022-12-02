from django.contrib import admin

from .models import Bot, Message, Variant


class BotAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner', 'start_message']
    list_filter = ('owner',)


class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'keyboard_type', 'bot']
    list_editable = ['keyboard_type']
    list_filter = ('bot',)


class VariantAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'current_message', 'next_message', 'display_bot']


admin.site.register(Bot, BotAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Variant, VariantAdmin)
