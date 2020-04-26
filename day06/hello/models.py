from django.db import models


class Project_User(models.Model):
    SEX=(
        (0, '女'),
        (1, '男'),
        (2, '保密'),
    )

    name = models.CharField(max_length=16, blank=False, null=False, help_text="姓名")
    password = models.CharField(max_length=20, blank=False, null=False, help_text="密码")
    phone = models.CharField(max_length=11, blank=True, null=True, help_text="手机")
    age = models.IntegerField(blank=True, null=True, help_text="年龄")
    sex = models.IntegerField(choices=SEX, blank=True, null=True, help_text="性别")
# Create your models here.
