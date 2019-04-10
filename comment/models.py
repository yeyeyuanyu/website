from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
# Create your models here.


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="user_comment", on_delete=models.CASCADE)

    root = models.ForeignKey("self", related_name="root_comment", null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", related_name="parent_comment", null=True, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User, related_name="reply_to_user", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['time']
