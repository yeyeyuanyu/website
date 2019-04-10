from django.shortcuts import render, redirect
from . import models
from . import forms
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
# Create your views here.


'''
def update_comment(request):
    user = request.user
    urls = request.META.get('HTTP_REFERER', reverse('website:home'))

    if not user.is_authenticated:
        return render(request, 'Animation_urls/error.html', {'error': '用户不存在', 'redirect': urls})

    text = request.POST.get('text','').strip()
    if text == '':
        return render(request, 'Animation_urls/error.html', {'error': '评论为空', 'redirect': urls})
    try:
        content_type = request.POST.get('content_type', '')
        object_id = int(request.POST.get('object_id', ''))
        model_class = ContentType.objects.get(model=content_type).model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except Exception as e:
        return render(request, 'Animation_urls/error.html', {'error': '评论对象不存在', 'redirect': urls})

    comment =models.Comment()
    comment.user = user
    comment.text = text
    comment.content_object = model_obj
    comment.save()

    return redirect(urls)
'''


def update_comment(request):
    # urls = request.META.get('HTTP_REFERER', reverse('website:home'))
    data = {}
    comment_form = forms.CommentForm(request.POST, user=request.user)
    if comment_form.is_valid():
        comment = models.Comment()
        comment.user = request.user
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_type']

        parent = comment_form.cleaned_data['parent']
        if parent is not None:
            comment.root = parent.root if parent.root is not None else parent
            comment.parent = parent
            comment.reply_to = parent.user
            data['reply_to'] = comment.reply_to.username
        else:
            data['reply_to'] = ''
        comment.save()
        # return redirect(urls)
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if comment.root is not None else ''

        data['status'] = 'SUCCESS'
        data['user'] = comment.user.username
        data['time'] = comment.time.strftime('%Y-%m-%d %H:%M:%S')
        data['text'] = comment.text
    else:
        data['status'] = 'ERROR'
        data['error'] = list(comment_form.errors.values())
        # return render(request, 'Animation_urls/error.html', {'error': comment_form.errors, 'redirect': urls})
    return JsonResponse(data)
