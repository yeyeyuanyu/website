from django import template
from comment.models import Comment
from django.contrib.contenttypes.models import ContentType
from Count.models import Count

register = template.Library()


@register.simple_tag
def comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()


@register.simple_tag
def read_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Count.objects.get(content_type=content_type, object_id=obj.pk).count_num

