#-*- conding:utf-8 -*-

from rest_framework import serializers
from .models import cms_NewsCatagory,News,Comment
from apps.catauth.serializer import UserSerializer

class NewsCatageorySerializer(serializers.ModelSerializer):
    class Meta:
        model = cms_NewsCatagory
        fields = ('id', 'name')

class NewsSerializer(serializers.ModelSerializer):
    catagory = NewsCatageorySerializer()
    author = UserSerializer()
    class Meta:
        model = News
        fields = ('id', 'title', 'desc', 'thumbnail', 'pub_time', 'catagory', 'author')

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Comment
        fields = ('id','content','pub_time','author')