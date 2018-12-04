from django.shortcuts import render
from django.middleware.csrf import get_token ,rotate_token
from .models import News,cms_NewsCatagory,Comment
from django.conf import  settings
from utils import restful
from .serializer import NewsSerializer,CommentSerializer
from django.http import Http404
from .forms import PublicCommentForm
from apps.catauth.decorators import cat_login_required_decorator

def news_index(request):
    get_token(request)
    count = settings.ONE_PAGE_NEWS_COUNT
    newses = News.objects.select_related('catagory','author').all()[0:count]

    catagories = cms_NewsCatagory.objects.all()
    context = {
        'newses' : newses,
        'catagories' : catagories,
    }
    return render(request,'news/news002.html',context=context)

def new_list(request):
    # 通过p参数来指定，获取第几页的数据
    # 并且这个p参数是通过查询字符串的方式传过去的/news/list/?p=2

    page = int(request.GET.get('p',1))
    catagory_id = int(request.GET.get('catagory_id',0))
    start = (page - 1) * settings.ONE_PAGE_NEWS_COUNT
    end = page * settings.ONE_PAGE_NEWS_COUNT
    if catagory_id == 0 :
    # newses = News.objects.order_by('-pub_time')[start:end].values()
        newses = News.objects.select_related('catagory','author').all()[start:end]
    else:
        newses = News.objects.select_related('catagory','author').filter(catagory_id=catagory_id)[start:end]
    serializer = NewsSerializer(newses, many=True)   # many = ture 是应对对象内容有多个,如这里newses的Queryset对象
    data = serializer.data
    return restful.result(data=data)



def news_details(request,news_id):
    get_token(request)
    try:
        news = News.objects.select_related('catagory','author').prefetch_related('comments__author').get(pk=news_id)
        context = {
            'news':news,
        }
        return render(request,'news/news-detail.html',context=context)
    except News.DoesNotExist:
        raise Http404

@cat_login_required_decorator
def public_comment(request):
    form = PublicCommentForm(request.POST)
    if form.is_valid():
        news_id = form.cleaned_data.get('news_id')
        content = form.cleaned_data.get('content')
        news = News.objects.get(pk=news_id)
        comment = Comment.objects.create(content=content,author=request.user,news=news)
        serialize = CommentSerializer(comment)
        data = serialize.data
        return restful.result(data=data)
    else:
        error = form.get_errors()
        return restful.params_error(message=error)

def search(request):
    return render(request, 'search/search.html')

