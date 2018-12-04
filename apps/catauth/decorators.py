#-*- conding:utf-8 -*-
from utils import restful
from django.shortcuts import redirect

def cat_login_required_decorator(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        else:
            if request.is_ajax():
                return restful.unauth(message='请先登录')
            else:
                return redirect("/")
    return wrapper