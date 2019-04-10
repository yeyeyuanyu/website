from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.fields import exceptions
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
# Create your models here.


class Count(models.Model):
    count_num = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class CountExpandMethod():
    def read_num(self):
        try:
            temp = ContentType.objects.get_for_model(self)
            count = Count.objects.get(content_type=temp, object_id=self.pk)
            return count.count_num
        except exceptions.ObjectDoesNotExist:
            return 0


class CountDate(models.Model):
    date = models.DateField(default=timezone.now)
    count_num = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

