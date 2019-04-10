from django.urls import path
from . import views

app_name = 'Animation_urls'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('user', views.user_page, name='user_page'),
    path('logout', views.logout, name='logout'),
    path('Animation_urls/', views.Animation_urls, name='Animation_urls'),
    path('Animation_urls//<int:Animation_id>/', views.add, name='add'),
    path('Animation_urls/save/', views.save, name='save'),
    path('Animation_urls/type/<int:type_id>/', views.animation_type, name='type'),
    path('Animation_urls/read/<int:Animation_id>/', views.read, name='read'),
    path('Animation_urls/details/<int:Animation_id>/', views.details, name='details'),
    # path('website/login', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('change_page/', views.change_page, name='change_page'),
    # path('change_user/', views.change_user, name='change_user'),
    path('login_page/', views.login_page, name='login_page'),
    path('code/', views.send_code, name='send_code'),
    # include在主路由（urls）的路径中包含应用中的路由
    # namespace是命名空间
]