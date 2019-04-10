from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_object', 'text', 'time', 'user', 'reply_to', 'parent', 'root',)
