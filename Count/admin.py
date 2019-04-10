from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Count)
class CountAdmin(admin.ModelAdmin):
    list_display = ('id', 'count_num', 'content_object', 'object_id')


@admin.register(models.CountDate)
class CountDateAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'count_num', 'content_object', 'object_id')
