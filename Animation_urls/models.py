from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
# from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from Count.models import CountExpandMethod, CountDate
# Create your models here.


class Type(models.Model):
    type_name = models.CharField(max_length=5)

    def __str__(self):
        return self.type_name


class Animation(models.Model, CountExpandMethod):
    img_website = models.TextField(null=True)
    form = models.ForeignKey(Type, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = RichTextField()  # RichTextUploadingField     # models.TextField(null=True)
    website = models.TextField(null=True)

    count_num = GenericRelation(CountDate)

    def __str__(self):
        return self.title

'''
class Read(models.Model):
    read = models.IntegerField(default=0)
    name = models.OneToOneField(Animation, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.read
'''
