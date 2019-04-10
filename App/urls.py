from django.urls import path
from . import views


app_name = 'App'
urlpatterns =[
    path('transform_page/', views.transform_page, name='transform_page'),
]
