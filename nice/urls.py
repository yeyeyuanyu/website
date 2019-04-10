from django.urls import path
from . import views

app_name = 'nice'

urlpatterns = [
   path('update_love', views.update_love, name='update_love'),
]
