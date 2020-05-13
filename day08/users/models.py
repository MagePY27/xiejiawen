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
        # 也可以在form里面写个方法来先加密然后再传到这里入库，那此处的seve方法就可以省略
        # password = form.cleaned_data['username]
        # form.instance.password = make_password(password)
        # form.instance = user = UserProfile.objects.get(pk=pk)
        print("kwargs:", self.password)
        print("keys:", self.__dict__)
        # 如果是创建用户，id号是不存在的，此时就对密码进行加密
        # 如果是修改用户，id号是有的，此时不对密码进行加密
        if self.id is None:
            self.password = make_password(self.password, None, 'pbkdf2_sha256')
            # 如果是修改密码，那么也对密码进行加密
        super(UserProfile, self).save(*args, **kwargs)


class Bar01(models.Model):
    """
    权限测试
    """
    name = models.CharField(max_length=255, null=True, )
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ("-created_at",)
        default_permissions = ()
        permissions = (
            ('view_bar01', '查看表'),
            ('add_bar01', '添加看表'),
        )

