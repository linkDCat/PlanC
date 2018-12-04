#-*- conding:utf-8 -*-

from django.urls import path,include
from . import  views

app_name = 'news'

urlpatterns = [
    path('',views.news_index,name='news_index'),
    path('<int:news_id>/',views.news_details,name='news_details'),
    path('list/',views.new_list,name='news_list'),
    path('comment/',views.public_comment,name='public_comment'),
]