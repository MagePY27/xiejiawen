from django.db import models

# Create your models here.

class User(models.Model):
    SEX=(
        (0, '男'), #object.get_字段名__display获取枚举型的数据
        (1, '女')
    )
    name = models.CharField(max_length=16, null=True, blank=True, help_text='姓名')
    password = models.CharField(max_length=20, null=True, blank=True, help_text='密码')
    phone = models.CharField(max_length=11, help_text='手机')
    age = models.IntegerField(help_text='年龄', null=True, blank=True)
    sex = models.IntegerField(choices=SEX, help_text='性别', null=True, blank=True)

    def __str__(self):
        return self.name, self.password, self.phone, self.age, self.sex

