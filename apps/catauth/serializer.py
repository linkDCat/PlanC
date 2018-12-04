#-*- conding:utf-8 -*-

from rest_framework import serializers
from .models import Front_User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Front_User
        fields = ('uid', 'telephone', 'username', 'email', 'is_staff', 'is_active')