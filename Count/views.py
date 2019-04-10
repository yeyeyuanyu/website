from django.shortcuts import render
import datetime
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from .models import Count, CountDate
from django.utils import timezone
from Animation_urls.models import Animation
from django.core.cache import cache
# Create your views here.


def add_count(request, obj):
    temp = ContentType.objects.get_for_model(obj)
    key = "%s_%d_read" % (temp.model, obj.pk)
    if not request.COOKIES.get(key):
        count, created = Count.objects.get_or_create(content_type=temp, object_id=obj.pk)
        count.count_num += 1
        count.save()

        date = timezone.now().date()
        count_date, created = CountDate.objects.get_or_create(content_type=temp, object_id=obj.pk, date=date)
        count_date.count_num += 1
        count_date.save()
        '''
        if CountDate.objects.filter(content_type=temp, object_id=obj.pk).count():
            count_date = CountDate.objects.get(content_type=temp, object_id=obj.pk)
        else:
            count_date = CountDate(content_type=temp, object_id=obj.pk)
        count_date.count_num += 1
        count_date.save()
        '''
    return key


def chart_seven(content_type):
    today = timezone.now().date()
    dates = []
    chart_result = []
    for i in range(6, -1, -1):
        date = today - datetime.timedelta(days=i)
        count_num_day = CountDate.objects.filter(content_type=content_type, date=date)

        dates.append(date.strftime('%m/%d'))
        result = count_num_day.aggregate(total=Sum('count_num'))
        chart_result.append(result['total'] or 0)

    return chart_result ,dates


def hot(content_type):
    hot_yestoday = cache.get('hot_yestoday')
    seven = cache.get('seven')

    today = timezone.now().date()
    hot_day = CountDate.objects.filter(content_type=content_type, date=today)
    hot_day = hot_day.order_by('-count_num')
    if seven is None:

        yestoday = today - datetime.timedelta(days=1)
        hot_yestoday = CountDate.objects.filter(content_type=content_type, date=yestoday)
        hot_yestoday = hot_yestoday.order_by('-count_num')
        '''
        hot_preive = []
        for day in range(6, 2, -1):
            yes_day = today - datetime.timedelta(days=day)
            yes_day = CountDate.objects.filter(content_type=content_type, date=yes_day)
            hot_preive.append(yes_day)
        hot_preive.append(hot_yestoday)
        hot_preive.append(hot_day)
        '''

        today = today + datetime.timedelta(days=1)
        dayed = today - datetime.timedelta(days=8)      # 小于                   # 大于
        seven = Animation.objects.filter(count_num__date__lt=today, count_num__date__gte=dayed)
        seven = seven.values('id', 'title').annotate(total=Sum('count_num__count_num')).order_by('-total')

        cache.set('hot_yestoday', hot_yestoday, 3600)
        cache.set('seven', seven, 3600)
    return hot_day[:3], hot_yestoday[:3], seven[:7]
