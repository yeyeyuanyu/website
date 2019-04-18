from django import forms
from django.contrib.auth import authenticate

from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', required=True
                               , widget=forms.TextInput(
                                        attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))

    password = forms.CharField(label='密码', required=True, widget=forms.PasswordInput(
                                        attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    '''
    def clean(self):
        super(LoginForm, self)
        username = self.cleaned_date['username']
        password = self.cleaned_data['password']

        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data
    '''


class RegForm(forms.Form):
    username = forms.CharField(label='用户名', required=True,
                               max_length=20,
                               min_length=3,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))

    email = forms.CharField(label='邮箱', required=False,
                            max_length=20,
                            widget=forms.EmailInput(
                                attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}))

    password = forms.CharField(label='密码', required=True,
                               min_length=6,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    password_again = forms.CharField(label='确认密码', required=True,
                                     min_length=6,
                                     widget=forms.PasswordInput(
                                         attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email == '':
            email = None
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email已存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']

        if password != password_again:
            raise forms.ValidationError('密码不一致')
        return password_again


class ChangeForm(forms.Form):
    username = forms.CharField(label='用户名', required=True,
                               max_length=20,
                               min_length=3,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': '请输入用户名', 'value': ''}))

    email = forms.CharField(label='邮箱', required=False,
                            max_length=20,
                            widget=forms.EmailInput(
                                attrs={'class': 'form-control', 'placeholder': '请输入邮箱', 'value': ''}))

    password = forms.CharField(label='密码', required=True,
                               min_length=6,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    password_again = forms.CharField(label='确认密码', required=True,
                                     min_length=6,
                                     widget=forms.PasswordInput(
                                         attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ChangeForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        if username != self.request.user.username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email != self.request.user.email:
            if email == '':
                email = None
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('email已存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']

        if password != password_again:
            raise forms.ValidationError('密码不一致')
        return password_again
