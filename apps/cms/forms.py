#-*- conding:utf-8 -*-

from django import forms
from apps.forms import FormMixin
from apps.news.models import News

class EditNewsCatagoryForm(forms.Form,FormMixin):
    pk = forms.IntegerField(error_messages={"required": "必须传入分类的id！"})
    name = forms.CharField(max_length=100)

class WriteNewsForm(forms.ModelForm,FormMixin):
    catagory = forms.IntegerField()
    class Meta:
        model = News
        exclude = ['catagory','pub_time','author']


class EditNewsForm(forms.ModelForm,FormMixin):
    catagory = forms.IntegerField()
    pk = forms.IntegerField()
    class Meta:
        model = News
        exclude = ['catagory', 'pub_time', 'author']