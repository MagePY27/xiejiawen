from django.db import models
from django.contrib.auth.models import AbstractUser


class Project_User(AbstractUser):
    types = (
        (1, '普通用户'),
        (2, '会员用户'),
        (3, '超级管理员'),
    )
    SEX=(
        (0, '女'),
        (1, '男'),
        (2, '保密'),
    )

    name = models.CharField(max_length=16, blank=False, null=False, help_text="姓名")
    password = models.CharField(max_length=20, blank=False, null=False, help_text="密码")
    user_type = models.IntegerField(choices=types, blank=False, null=False, help_text="用户类型", default=1)
    phone = models.CharField(max_length=11, blank=True, null=True, help_text="手机")
    age = models.IntegerField(blank=True, null=True, help_text="年龄")
    sex = models.IntegerField(choices=SEX, blank=True, null=True, help_text="性别")
# Create your models here.
