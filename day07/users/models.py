from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password


class UserProfile(AbstractUser):
    types = [
        (0, '超级管理员'),
        (1, '权限用户'),
        (2, '普通用户'),
    ]

    SEX = [
        (0, '男'),
        (1, '女'),
        (2, '保密'),
    ]

    name = models.CharField(max_length=128, blank=True)
    phone = models.CharField(max_length=11, blank=True)
    password = models.CharField(max_length=128, blank=False)
    age = models.IntegerField(blank=True, default=18)
    sex = models.IntegerField(choices=SEX, blank=True, default=0)
    user_type = models.IntegerField(choices=types, default=2, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.password = make_password(self.password, None, 'pbkdf2_sha256')
        super(UserProfile, self).save(*args, **kwargs)