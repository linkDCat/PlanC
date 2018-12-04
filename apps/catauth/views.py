from django.shortcuts import render
from django.contrib.auth import login,logout,authenticate
from django.views.decorators.http import require_POST
from .forms import login_form,register_form
from django.http import JsonResponse,HttpResponse
from utils import restful
from django.middleware.csrf import get_token ,rotate_token
from django.shortcuts import redirect,reverse
from utils.captcha import catcaptcha
from io import BytesIO
from django.core.cache import cache
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()

@require_POST
def login_view(request):
    get_token(request)
    form = login_form(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request,username=telephone,password=password)

        if user:
            if user.is_active:
                login(request,user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return restful.ok()

            else:
                return restful.unauth(message="您的账号已经被冻结了！")

        else:
            return restful.params_error(message="您的手机号码或密码错误！")

    else:
        errors = form.get_errors()
        return restful.params_error(message=errors)

def logout_view(request):
    logout(request)
    return redirect(reverse('index'))

@require_POST
def register(request):
    form = register_form(request.POST)
    get_token(request)
    if form.is_valid():
        telephone = form.cleaned_data.get("telephone")
        password = form.cleaned_data.get("password1")
        username = form.cleaned_data.get("username")

        user = User.objects.create_user(telephone=telephone,password=password,username=username)
        login(request,user)
        return restful.ok()
    else :
        errors = form.get_errors()
        return restful.params_error(message=errors)


def img_captcha(request):
    text,image = catcaptcha.Captcha.gene_code()
    # BytesIO：相当于一个管道，用来存储图片的流数据
    out = BytesIO()
    # 调用image的save方法，将这个image对象保存到BytesIO中
    image.save(out,'png')
    # 将BytesIO的文件指针移动到最开始的位置
    out.seek(0)

    response = HttpResponse(content_type='image/png')
    # 从BytesIO的管道中，读取出图片数据，保存到response对象上
    response.write(out.read())
    response['Content-length'] = out.tell()

    # 12Df：12Df.lower()
    cache.set(text.lower(),text.lower(),5*60)

    return response

def sms_captcha(request):
    # /sms_captcha/?telephone=xxx
    telephone = request.GET.get('telephone')
    code = catcaptcha.Captcha.gene_text()
    cache.set(telephone,code,300)
    print('短信验证码：',code)
    # result = aliyunsms.send_sms(telephone,code)
    return restful.ok()

def cache_test(request):
    cache.set('username','cat',120)
    result = cache.get('username')
    print(result)
    return HttpResponse('success')



