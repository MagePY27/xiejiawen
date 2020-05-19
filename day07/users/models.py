from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    types = (
        (0, '超级管理员'),
        (1, '普通权限用户'),
        (2, '非法用户'),
    )
    SEX = (
        (0, '男'),
        (1, '女'),
        (2, '保密'),
    )
    name = models.CharField(max_length=128)
    age = models.IntegerField()
    sex = models.IntegerField(choices=SEX)
    user_type = models.IntegerField(choices=types)
    phone = models.CharField(max_length=11, blank=True)
# Create your models here.
