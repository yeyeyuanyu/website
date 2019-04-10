from django import template
from nice.models import LoveCount, LoveRecord
from django.contrib.contenttypes.models import ContentType


register = template.Library()


@register.simple_tag
def love_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    loves, created = LoveCount.objects.get_or_create(content_type=content_type, object_id=obj.pk)
    return loves.love_num


@register.simple_tag(takes_context=True)
def love_active(context, obj):
    user = context['user']
    if not user.is_authenticated:
        return ''
    content_type = ContentType.objects.get_for_model(obj)
    if LoveRecord.objects.filter(content_type=content_type, object_id=obj.pk, user=user).exists():
        return 'active'
    else:
        return ''
