from django.db import models


class User(models.Model):  #
    SEX = (
        (0, '男'), #object.get_字段名__display获取枚举型的数据
        (1, '⼥'),
    )
    name = models.CharField(max_length=20,
                            help_text="用户名 ")
    password = models.CharField(max_length=32, help_text="密码")
    sex = models.IntegerField(choices=SEX, null=True, blank=True)
    age = models.IntegerField(help_text='年龄', null=True, blank=True)



    def __str__(self):  #
        return "name is {}, password is {}, SEX is {}, age is {}".format(self.name, self.password, self.sex, self.age)