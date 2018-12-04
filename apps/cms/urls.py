from django.urls import path
from . import views

app_name='cms'

urlpatterns= [
    path('',views.cms_index,name='cms_index'),
    path('login/',views.login_view,name='login'),
    path('news/',views.WriteNewsView.get,name='cms_wirtenews_page'),
    path('news_list/',views.NewsListView.as_view(),name='cms_news_list'),
    path('edit_news/',views.EditNewsView.as_view(),name='cms_edit_news'),
    path('delete_news/',views.NewsListView.delete_news,name='cms_delete_news'),
    path('write_news/',views.WriteNewsView.post,name='cms_wirtenews'),
    path('news_catagory/',views.WriteNewsView.news_catagory,name='cms_news_catagory'),
    path('add_news_catagory/',views.WriteNewsView.add_news_catagory,name='add_news_catagory'),
    path('edit_news_catagory/',views.WriteNewsView.edit_news_catagory,name='edit_news_catagory'),
    path('delete_news_catagory/',views.WriteNewsView.delete_news_catagory,name='delete_news_catagory'),
    path('upload_file/',views.WriteNewsView.upload_file,name='upload_file'),
]