from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')


@admin.register(models.Animation)
class AnimationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'form', 'content', 'read_num')


'''
@admin.register(models.Read)
class ReadAdmin(admin.ModelAdmin):
    list_display = ( 'id' , 'read', 'name')
'''
