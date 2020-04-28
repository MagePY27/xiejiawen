from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from hello.models import User
import re

# 原生表单验证各种表单类型以及自定义


# name = forms.CharField(max_length=12, required=True)
# password = forms.CharField(min_length=8,  max_length=16, required=True)
# phone = forms.CharField(max_length=11, required=False)
# age = forms.IntegerField(max_value=100, required=False)
# sex = forms.IntegerField(required=False)
# skill = forms.CharField(max_length=10, required=False)
# file = forms.FileField()
# info = forms.CharField(max_length=100, required=True)

# 自定义验证格式， clean_字段
"""
    Django的form系统自动寻找匹配的函数方法，该方法以clean_开头，并以字段名称结束。
    如果有这样的方法，那么它将在校验时被调用， clean_info()方法将在指定字段的默认校验逻辑
    执行之后被调用。
    本例中，在必填CharField这个校验逻辑之后， 因为字段数据已被部分处理，所以它被从self.cleaned_data
    中提取出来，同样我们不必担心数据是否为空，因为它已被校验过了。
"""


class UserModelForm(forms.ModelForm):
    class Meta:
        # 与model建立了依赖关系， 即按照model中的字段类型来验证
        model = User
        # 根据model定义的类型，验证所有列的属性
        fields = "__all__"
        # 或者指定某些列
        # fields = ['name', 'password', 'age']

    # 对字段进行二次验证
    def clean_phone(self):
        """
        通过正则表达式验证手机号是否合法
        """
        phone = self.cleaned_data['phone']
        phone_regex = r'^1[3578][0-9]{9}$'
        p = re.compile(phone_regex)
        if p.match(phone):
            return phone
        else:
            # 自定义表单错误
            raise forms.ValidationError("手机号非法", code='invalid')


class UserUpdateModelForm(forms.ModelForm):
    # 密码确认字段，model里不存在，此处要加上去
    confirm_password = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['name', 'password', 'phone', 'age', 'sex']

    def clean_phone(self):
            phone = self.cleaned_data['phone']
            phone_regex = r'^1[3578][0-9]{9}$'
            p = re.compile(phone_regex)
            if p.match(phone):
                return phone
            else:
                # 自定义表单错误
                raise forms.ValidationError("手机号非法", code='invalid')

    def clean_confirm_password(self):
            password = self.cleaned_data['password']
            confirm_password = self.cleaned_data['confirm_password']
            if password != confirm_password:
                raise forms.ValidationError('两次输入的密码不一致', code="password_mismatch")
            return confirm_password

    # def clean_info(self):
    #     print(self.cleaned_data)
    #     info = self.cleaned_data['info']
    #     num_info = len(info.strip())
    #     print("info长度为:", num_info)
    #     if num_info < 4:
    #         raise forms.ValidationError('info too short')
    #     return info

    # def clean_name(self):
    #     name = self.cleaned_data['name']
    #     print(self.cleaned_data)
    #     num_name = len(name.strip())
    #     if not name:
    #         raise forms.ValidationError('name is Required Field!')
    #     if num_name > 12:
    #         raise forms.ValidationError('name is too long')
    #     return name
    #
    # def clean_password(self):
    #     password = self.cleaned_data['password']
    #     num_password = len(password.strip())
    #     if not password:
    #         raise forms.ValidationError('password is Required Field!')
    #     if num_password < 8 or num_password >16:
    #         raise forms.ValidationError('password is longer than 16 or shorter than 8')
    #     # return "密码长度为:{}".format(password)
    #     return password
    #
    # def clean_age(self):
    #     age = self.cleaned_data['age']
    #     if not age:
    #         age=18
    #     elif int(age) > 100 or int(age) < 0:
    #             raise forms.ValidationError('invalid age format!')
    #     # return "年龄为:{}".format(age)
    #     return age
    #
    # def clean_sex(self):
    #     sex = self.cleaned_data['sex']
    #     return sex
