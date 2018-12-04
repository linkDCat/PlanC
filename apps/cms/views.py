from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_POST,require_GET
from apps.news.models import cms_NewsCatagory,News
from utils import restful
from apps.cms.forms import EditNewsCatagoryForm,WriteNewsForm,EditNewsForm
import os
from django.conf import settings
from django.core.paginator import Paginator
from datetime import datetime
from django.utils.timezone import make_aware
from urllib import parse
# Create your views here.

def login_view(request):
    return render(request,'cms/login.html')

@staff_member_required(login_url='index')
def cms_index(request):
    return render(request,'cms/cms_index.html')

class WriteNewsView(View):
    def get(request):
        catagories = cms_NewsCatagory.objects.all()
        context = {
            'catagories':catagories,
        }
        return render(request,'cms/cms_writenews.html',context=context)

    def post(request):
        form = WriteNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            catagory_id = form.cleaned_data.get('catagory')
            catagory = cms_NewsCatagory.objects.get(pk=catagory_id)
            News.objects.create(title=title,desc=desc,thumbnail=thumbnail,content=content,catagory=catagory,author=request.user)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())

    @require_POST
    def upload_file(request):
        file = request.FILES.get('file')
        name = file.name
        fileurl = os.path.join(settings.MEDIA_ROOT,name)
        with open(fileurl,'wb') as fp:
            for chunk in file.chunks():
                fp.write(chunk)
        url = request.build_absolute_uri(settings.MEDIA_URL+name)
        # http://127.0.1:8000/media/abc.jpg
        return restful.result(data={'url':url})



    @require_GET
    def news_catagory(request):
        catagories = cms_NewsCatagory.objects.all()
        context = {
            'catagories' : catagories
        }
        return render(request,'cms/cms_newsCatagory.html',context=context)

    @require_POST
    def add_news_catagory(request):
        name = request.POST.get('name')
        exists = cms_NewsCatagory.objects.filter(name=name).exists()
        if not exists:
            cms_NewsCatagory.objects.create(name=name)
            return restful.ok()
        else:
            return restful.params_error(message='该分类已经存在')

    @require_POST
    def edit_news_catagory(request):
        form = EditNewsCatagoryForm(request.POST)
        if form.is_valid():
            pk = form.cleaned_data.get('pk')
            name = form.cleaned_data.get('name')

            try:
                cms_NewsCatagory.objects.filter(pk=pk).update(name=name)
                return restful.ok()
            except:
                return restful.params_error(message='该分类不存在')
        else:
            errors = form.get_errors()
            return restful.params_error(message=errors)

    @require_POST
    def delete_news_catagory(request):
        pk = request.POST.get('pk')
        try:
            cms_NewsCatagory.objects.filter(pk=pk).delete()
            return restful.ok()
        except:
            return restful.params_error(message='该分类不存在')

class EditNewsView(View):
    def get(self,request):
        news_id = request.GET.get('news_id')
        news = News.objects.get(pk=news_id)
        context ={
            'news': news,
            'catagories':cms_NewsCatagory.objects.all(),
        }
        return render(request,'cms/cms_writenews.html',context=context)

    def post(self,request):
        form = EditNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            catagory_id = form.cleaned_data.get('catagory')
            pk = form.cleaned_data.get('pk')
            catagory = cms_NewsCatagory.objects.get(pk=catagory_id)
            News.objects.filter(pk=pk).update(title=title,desc=desc,thumbnail=thumbnail,content=content,catagory=catagory)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())

class NewsListView(View):
    def get(self,request):
        page = int(request.GET.get('p',1))
        start = request.GET.get('start')
        end =request.GET.get('end')
        title = request.GET.get('title')
        catagory_id = int(request.GET.get('catagory',0)or 0)

        newses = News.objects.select_related('catagory', 'author')

        if start or end:
            if start:
                start_datatime = datetime.strptime(start,'%Y/%m/%d')
            else:
                start_datatime = datetime(year=2018,month=11,day=22)

            if end :
                end_datatime = datetime.strptime(end,'%Y/%m/%d')
            else:
                end_datatime = datetime.today()

            newses =newses.filter(pub_time__range=(make_aware(start_datatime),make_aware(end_datatime)))

        if title :
            newses=newses.filter(title__icontains=title)

        if catagory_id:
            newses=newses.filter(catagory=catagory_id)

        catagories = cms_NewsCatagory.objects.all()

        paginator = Paginator(newses, 5)
        page_obj = paginator.page(page)

        context_data = self.get_pagination_data(paginator, page_obj)

        context = {
            'newses':page_obj.object_list,
            'catagories': catagories,
            'page_obj': page_obj,
            'paginator': paginator,
            'start': start,
            'end' : end,
            'title' : title,
            'catagory_id':catagory_id,
            'url_query':'&'+parse.urlencode({
                'start':start or '',
                'end':end or '',
                'catagory':catagory_id or '',
                'title':title or '',
            }),
        }
        context.update(context_data)
        return render(request,'cms/cms_newsList.html',context=context)



    def get_pagination_data(self,paginator,page_obj,around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1,current_page)
        else:
            left_has_more = True
            left_pages = range(current_page-around_count,current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page+1,num_pages+1)
        else:
            right_has_more = True
            right_pages = range(current_page+1,current_page+around_count+1)

        return {
            # left_pages：代表的是当前这页的左边的页的页码
            'left_pages': left_pages,
            # right_pages：代表的是当前这页的右边的页的页码
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }

    def delete_news(request):
        news_id = request.POST.get('news_id')
        News.objects.filter(pk=news_id).delete()
        return restful.ok()