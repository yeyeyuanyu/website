from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.LoveCount)
class AdminLoveCount(admin.ModelAdmin):
    list_display = ('id', 'object_id', 'love_num')


@admin.register(models.LoveRecord)
class AdminLoveRecord(admin.ModelAdmin):
    list_display = ('id', 'object_id', 'user', 'love_time')
