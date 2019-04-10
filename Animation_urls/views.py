from django.shortcuts import render, get_object_or_404, redirect
from . import models
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from Count.views import add_count, chart_seven, hot
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from comment.models import Comment
from comment.forms import CommentForm
from .forms import LoginForm, RegForm, ChangeForm
from django.http import JsonResponse
from django.core.mail import send_mail
import string
import random
# from django.db.models import Count

# Create your views here.


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('website:home')))


def user_page(request):
    dictionary = {}
    dictionary['change_form'] = ChangeForm()
    return render(request, 'Animation_urls/user_page.html', dictionary)


def change_page(request):
    dictionary = {}
    if request.method == 'POST':
        data = {}
        change_form = ChangeForm(request.POST, request=request)
        dictionary['change_form'] = change_form

        if change_form.is_valid():

            username = change_form.cleaned_data['username']
            email = change_form.cleaned_data['email']
            password = change_form.cleaned_data['password']

            user = request.user
            '''
            if username != user.username:
                if User.objects.filter(username=username).exists():
                    raise forms.ValidationError('用户名已存在')
            if email != user.email:
                if User.objects.filter(email=email).exists():
                    raise forms.ValidationError('邮箱已绑定')
            '''
            user = User.objects.get(username=user.username)
            user.username = username
            if email is None or '':
                pass
            else:
                user.email = email
            user.set_password(password)
            user.save()
            del request.session['email_code']

            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            # return redirect(request.GET.get('from', reverse('website:home')))
            return redirect(request.GET.get('from', reverse('website:home')))
    else:
        dictionary['change_form'] = ChangeForm()
        return render(request, 'Animation_urls/change_page.html', dictionary)
    return render(request, 'Animation_urls/change_page.html', dictionary)


'''
def change_user(request):
    dictionary = {}
    data = {}
    change_form = ChangeForm(request.POST, request=request)
    dictionary['change_form'] = change_form

    if change_form.is_valid():

        username = change_form.cleaned_data['username']
        email = change_form.cleaned_data['email']
        password = change_form.cleaned_data['password']

        user = request.user
        
        
        
        
        if username != user.username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('用户名已存在')
        if email != user.email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('邮箱已绑定')
 
        data['status'] = "SUCCESS"
        user = User.objects.get(username=user.username)
        user.username = username
        if email is None or '':
            return redirect(request.GET.get('from', reverse('website:home')))
        else:
            user.email = email
            authenticate_code = change_form.cleaned_data['authenticate_code']
            if authenticate_code == '':
                data['status'] = "ERROR"
                return render(request, 'Animation_urls/change_page.html', dictionary)
            else:
                pass
        user.set_password(password)
        user.save()

        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)
        # return redirect(request.GET.get('from', reverse('website:home')))
    return render(request, 'Animation_urls/change_page.html', dictionary)
'''


def send_code(request):
    data = {}
    email = request.GET.get('email', '')
    if email != '':
        code = random.sample(string.ascii_letters + string.digits, 5)
        code = ''.join(code)
        request.session['email_code'] = code
        send_mail(
            '绑定邮箱',  # Subject here
            '验证码: %s ' % code,  # Here is the message
            '878928552@qq.com',
            [email],
            fail_silently=False,
        )
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def home_page(request):
    content_type = ContentType.objects.get_for_model(models.Animation)
    chart, dates  = chart_seven(content_type)
    dictionary = {}
    dictionary['chart'] = chart
    dictionary['dates'] = dates
    return render(request, 'Animation_urls/home_page.html', dictionary)


def Animation_urls(request):
    dictionary = {}
    Animation = models.Animation.objects.all()  # 获取Animation_urls的所有对象
    dictionary['type'] = models.Type.objects.all()
    page_s = Paginator(Animation, 2)
    pages = request.GET.get('page', 1)
    dictionary['Animation'] = page_s.get_page(pages)
    content_type = ContentType.objects.get_for_model(models.Animation)
    day, yestoday, seven_day = hot(content_type)
    dictionary['day'] = day
    dictionary['yestoday'] = yestoday
    dictionary['seven_day'] = seven_day
    return render(request, 'Animation_urls/Animation_urls.html', dictionary)


def details(request, Animation_id):
    Animation = get_object_or_404(models.Animation, pk=Animation_id)
    content_type = ContentType.objects.get_for_model(Animation)
    comments = Comment.objects.filter(content_type=content_type, object_id=Animation.pk, parent=None)
    dictionary = {}

    data = {}
    data['content_type'] = content_type.model
    data['object_id'] = Animation_id
    data['reply_comment_id'] = 0
    dictionary['comment_form'] = CommentForm(initial=data)

    dictionary['Animation'] = Animation
    dictionary['comments'] = comments.order_by('-time')
    return render(request, 'Animation_urls/Animation_details.html', dictionary)


'''
def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(request, username=username, password=password)
    urls = request.META.get('HTTP_REFERER', reverse('website:home'))
    if user is not None:
        auth.login(request, user)
        return redirect(urls)
    else:
        return render(request, urls, {'error': '用户不存在', 'redirect': urls})
'''


def add(request, Animation_id):
    dictionary = {}
    if str(Animation_id) == '0':
        return render(request, 'Animation_urls/add.html')
    if str(Animation_id) != '0':
        # Animation = models.Animation.objects.get(pk=Animation_id)
        dictionary['Animation'] = get_object_or_404(models.Animation, pk=Animation_id)
        return render(request, 'Animation_urls/add.html', dictionary)


def save(request):
    dictionary = {}
    Animation_id = request.POST['Animation_id']
    title = request.POST['title']
    img_websie = request.POST['img_website']
    content = request.POST['content']
    website = request.POST['website']
    if str(Animation_id) == '0':
        models.manhuan.objects.create(title=title, img_websie=img_websie, content=content, website=website)
    if str(Animation_id) != '0':
        Animation = models.Animation.objects.get(pk=Animation_id)
        Animation.title = title
        Animation.content = content
        Animation.img_website = img_websie
        Animation.website = website
        Animation.save()
    Animation = models.Animation.objects.all()  # 获取Animation_urls的所有对象
    dictionary['type'] = models.Type.objects.all()
    page_s = Paginator(Animation, 2)
    pages = request.GET.get('page', 1)
    dictionary['Animation'] = page_s.get_page(pages)
    return render(request, 'Animation_urls/Animation_urls.html', dictionary)


def animation_type(request, type_id):
    if str(type_id) == '0':
        Animation = models.Animation.objects.all()
    else:
        type_name = get_object_or_404(models.Type, pk=type_id)
        Animation = models.Animation.objects.filter(form=type_name)

    dictionary = {}
    dictionary['type'] = models.Type.objects.all()
    dictionary['type_id'] = type_id
    page_s = Paginator(Animation, 2)
    pages = request.GET.get('page', 1)
    dictionary['Animation'] = page_s.get_page(pages)

    content_type = ContentType.objects.get_for_model(models.Animation)
    day, yestoday, seven_day = hot(content_type)
    dictionary['day'] = day
    dictionary['yestoday'] = yestoday
    dictionary['seven_day'] = seven_day

    return render(request, 'Animation_urls/Animation_urls.html', dictionary)


def read(request, Animation_id):
    dictionary = {}
    Animation = get_object_or_404(models.Animation, pk=Animation_id)
    read_cookies = add_count(request, Animation)

    '''
    if not request.COOKIES.get('Animation_%s_read' % Animation_id):
        temp = ContentType.objects.get_for_model(models.Animation)

        if Count.objects.filter(content_type=temp, object_id=Animation_id).count():

            count = Count.objects.get(content_type=temp, object_id=Animation_id)
        else:
            count = Count(content_type=temp, object_id=Animation_id)

        count.count_num += 1
        count.save()
        
        _________________________________________________________________________
        
        if models.Read.objects.filter(name=Animation).count():
            read = models.Read.objects.get(name=Animation)
        else:
            read = models.Read(name=Animation)
        read.read += 1
        read.save()
        '''

    type_id = request.GET.get('type_id')
    if str(type_id) == '0':
        Animation = models.Animation.objects.all()
    else:
        type_name = get_object_or_404(models.Type, pk=type_id)
        Animation = models.Animation.objects.filter(form=type_name)
    dictionary['type_id'] = int(type_id)
    dictionary['type'] = models.Type.objects.all()
    page_s = Paginator(Animation, 2)
    page_number = request.GET.get('page_number')
    pages = request.GET.get('page', page_number)
    dictionary['page_number'] = page_number
    dictionary['Animation'] = page_s.get_page(pages)

    content_type = ContentType.objects.get_for_model(models.Animation)
    day, yestoday, seven_day = hot(content_type)
    dictionary['day'] = day
    dictionary['yestoday'] = yestoday
    dictionary['seven_day'] = seven_day

    response = render(request, 'Animation_urls/Animation_urls.html', dictionary)
    response.set_cookie(read_cookies, 'true', max_age=60)
    return response


def login_page(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect(request.GET.get('from', reverse('website:home')))
            else:
                login_form.add_error(None, '用户名或密码不正确')
    else:
        login_form = LoginForm()
    dictionary ={}
    urls = request.META.get('HTTP_REFERER', reverse('website:home'))
    dictionary['urls'] = urls
    dictionary['login_form'] = login_form
    return render(request, 'Animation_urls/login.html', dictionary)


'''
def login_page(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('website:home')))
    else:
        login_form = LoginForm()

    dictionary ={}
    dictionary['login_form'] = login_form
    return render(request, 'Animation_urls/login.html', dictionary)
'''


def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']

            user = User.objects.create_user(username, email, password)
            user.save()
            '''
            user = User()
            user.username = username
            user.email = email
            user.set_password(password)
            user.save()
            '''
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('website:home')))
    else:
        reg_form = RegForm()

    dictionary = {}
    urls = request.META.get('HTTP_REFERER', reverse('website:home'))
    dictionary['urls'] = urls
    dictionary['register_form'] = reg_form
    return render(request, 'Animation_urls/register.html', dictionary)
