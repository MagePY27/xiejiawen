from django.db import models

# Create your models here.

class User(models.Model):
    SEX = (
        (0, '男'), #object.get_字段名__display获取枚举型的数据
        (1, '⼥'),
    )
    name = models.CharField(max_length=20, help_text='姓名')
    password = models.CharField(max_length=20, help_text='密码')
    age = models.IntegerField(help_text='年龄', null=True, blank=True)
    sex = models.IntegerField(choices=SEX, null=True, blank=True)

    def __str__(self):
        return self.name, self.password, self.age, self.sex
