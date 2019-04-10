from django.shortcuts import render
from django.http import JsonResponse
from .models import LoveRecord, LoveCount
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
# Create your views here.


def success_response(love):
    data = {}
    data['status'] = 'SUCCESS'
    data['love'] = love
    return JsonResponse(data)


def error_response(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


def update_love(request):
    user = request.user
    if not user.is_authenticated:
        return error_response(400, 'you were not login')

    object_id = request.GET.get('object_id')
    content_type = request.GET.get('content_type')
    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return error_response(401, 'object not exist')

    if request.GET.get('is_love') == 'true':  # 前端点赞
        record_love, created = LoveRecord.objects.get_or_create(user=user, content_type=content_type,
                                                                object_id=object_id)
        if created:
            count_love, created = LoveCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            count_love.love_num += 1
            count_love.save()
            return success_response(count_love.love_num)
        else:
            # 以经点赞
            return error_response(402, 'you were loved')

    else:  # 取消点赞
        if LoveRecord.objects.filter(user=user, content_type=content_type, object_id=object_id).exists():
            record_love = LoveRecord.objects.get(user=user, content_type=content_type, object_id=object_id)
            record_love.delete()

            count_love, created = LoveCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                count_love.love_num -= 1
                count_love.save()
                return success_response(count_love.love_num)
            else:
                return error_response(404, 'data error')
        else:
            # 没有点赞过
            return error_response(403, 'you were not loved')
