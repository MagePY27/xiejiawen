import re
from django import forms
from hello.models import UserProfile
from datetime import datetime


class UserLoginForm(forms.Form):
    username = forms.CharField(required=True, error_messages={"required": "请填写用户名"})
    password = forms.CharField(required=True, error_messages={"required": "请填写密码"})

    def clean_username(self):
        if "username" not in self.cleaned_data.keys():
            raise forms.ValidationError("用户名为必填项", code="ValueErr")
        else:
            username = self.cleaned_data['username']
            if len(username.strip()) > 16:
                raise forms.ValidationError("你的名字太长了")
            elif len(username.strip()) < 2:
                raise forms.ValidationError("名字至少要包含两个字或字符")
            else:
                return username

    def clean_password(self):
        # print("pwd:", self.cleaned_data)
        password = self.cleaned_data["password"]
        return password


class UserCreateForm(forms.ModelForm):
    """
    要先建函数获取表单中的各个字段，不然会报字段不存在
    """
    confirm_password = forms.CharField(required=True)

    class Meta:
        model = UserProfile
        fields = "__all__"

    def clean_username(self):
        # 应该再加一个特殊字符的判断
        if "username" not in self.cleaned_data.keys():
            raise forms.ValidationError("用户名为必填项", code="ValueErr")
        else:
            username = self.cleaned_data['username']
            # 除去名字两端的空字符，按道理说应该去掉名字上的所有特殊字符
            if len(username.strip()) > 16:
                raise forms.ValidationError("你的名字太长了")
            elif len(username.strip()) < 2:
                raise forms.ValidationError("名字至少要包含两个字或字符")
            else:
                return username

    def clean_password(self):
        if "password" not in self.cleaned_data.keys():
            raise forms.ValidationError("密码为必填项", code="ValueErr")
        else:
            password = self.cleaned_data['password']
            if len(password.strip()) < 8 or len(password.strip()) > 16:
                raise forms.ValidationError("你的密码太长或太短")
            else:
                return password

    def clean_confirm_password(self):
        if "password" not in self.cleaned_data.keys():
            raise forms.ValidationError("密码为必填项", "ValueErr")
        else:
            password = self.cleaned_data["password"]
            # 首先判断密码是否非空
            if "confirm_password" not in self.cleaned_data.keys():
                raise forms.ValidationError("密码为必填项", code="ValueErr")
            else:
                confirm_password = self.cleaned_data["confirm_password"]
                if confirm_password != password:
                    raise forms.ValidationError("两次密码不一致", code="MismatchErr")
                # 两个字段相等才能到这一步，这一步直接判断password的长度即可，密码可能包含空格，因此不使用strip
                elif len(password) < 8 or len(password) > 16:
                    raise forms.ValidationError("密码太长或太短", code="invalid")
                else:
                    return confirm_password

    def clean_phone(self):
        if "phone" not in self.cleaned_data.keys():
            raise forms.ValidationError("手机为必填项")
        else:
            phone = self.cleaned_data["phone"]
            if not phone:
                raise forms.ValidationError("手机为必填项")
            else:
                phone_regex = re.compile(r"^1[3|5|7|8][0-9]{9}$")
            if phone_regex.match(phone):
                return phone
            else:
                raise forms.ValidationError("手机号不合法", code="invalid")

    def clean_age(self):
        if "age" not in self.cleaned_data.keys():
            raise forms.ValidationError("年龄为必填项", code="invalid")
        else:
            age = self.cleaned_data["age"]
            if age > 150:
                raise forms.ValidationError("年龄不应该超过150", code="invalid")
            elif age < 0:
                raise forms.ValidationError("年龄不应该小于0", code="invalid")
            else:
                return age

    def clean_sex(self):
        if "sex" not in self.cleaned_data.keys():
            self.cleaned_data["sex"] = 0
        else:
            sex = self.cleaned_data["sex"]
        return sex

    def clean_user_type(self):
        if "user_type" not in self.cleaned_data.keys():
            # 默认用户为普通用户
            self.cleaned_data["user_type"] = 1
        else:
            user_type = self.cleaned_data["user_type"]
        return user_type

    def clean_date_joined(self):
        if "date_joined" not in self.cleaned_data.keys():
            self.cleaned_data["date_joined"] = date
        else:
            date_joined = self.cleaned_data["date_joined"]
        return date_joined



class UserModefyForm(forms.ModelForm):
    confirm_password = forms.CharField(required=True)

    class Meta:
        model = UserProfile
        fields = "__all__"

    def clean_username(self):
        # 应该再加一个特殊字符的判断
        if "username" not in self.cleaned_data.keys():
            raise forms.ValidationError("用户名为必填项", code="ValueErr")
        else:
            username = self.cleaned_data['username']
            # 除去名字两端的空字符，按道理说应该去掉名字上的所有特殊字符
            if len(username.strip()) > 16:
                raise forms.ValidationError("你的名字太长了")
            elif len(username.strip()) < 2:
                raise forms.ValidationError("名字至少要包含两个字或字符")
            else:
                return username

    def clean_password(self):
        if "password" not in self.cleaned_data.keys():
            raise forms.ValidationError("密码为必填项", code="ValueErr")
        else:
            password = self.cleaned_data['password']
            if len(password.strip()) < 8 or len(password.strip()) > 16:
                raise forms.ValidationError("你的密码太长或太短")
            else:
                return password

    def clean_confirm_password(self):
        if "password" not in self.cleaned_data.keys():
            raise forms.ValidationError("password字段不合法", "ValueErr")
        else:
            password = self.cleaned_data["password"]
            # 首先判断密码是否非空
            if "confirm_password" not in self.cleaned_data.keys():
                raise forms.ValidationError("密码为必填项", code="ValueErr")
            else:
                confirm_password = self.cleaned_data["confirm_password"]
                if confirm_password != password:
                    raise forms.ValidationError("两次密码不一致", code="MismatchErr")
                # 两个字段相等才能到这一步，这一步直接判断password的长度即可，密码可能包含空格，因此不使用strip
                elif len(password) < 8 or len(password) > 16:
                    raise forms.ValidationError("密码太长或太短", code="invalid")
                else:
                    return confirm_password

    def clean_phone(self):
        if "phone" not in self.cleaned_data.keys():
            raise forms.ValidationError("手机为必填项")
        else:
            phone = self.cleaned_data["phone"]
            phone_regex = re.compile(r"^1[3|5|7|8][0-9]{9}$")
            if phone_regex.match(phone):
                return phone
            else:
                raise forms.ValidationError("手机号不合法", code="invalid")

    def clean_age(self):
        if "age" not in self.cleaned_data.keys():
            raise forms.ValidationError("年龄为必填项", code="invalid")
        else:
            age = self.cleaned_data["age"]
            if age > 150:
                raise forms.ValidationError("年龄不应该超过150", code="invalid")
            elif age < 0:
                raise forms.ValidationError("年龄不应该小于0", code="invalid")
            else:
                return age

    def clean_sex(self):
        if "sex" not in self.cleaned_data.keys():
            self.cleaned_data["sex"] = 0
        else:
            sex = self.cleaned_data["sex"]
        return sex

    def clean_user_type(self):
        if "user_type" not in self.cleaned_data.keys():
            # 默认用户为普通用户
            self.cleaned_data["user_type"] = 1
        else:
            user_type = self.cleaned_data["user_type"]
        return user_type

    def clean_date_joined(self):
        date = datetime.now()
        if "date_joined" not in self.cleaned_data.keys():
            self.cleaned_data["date_joined"] = date
        else:
            date_joined = self.cleaned_data["date_joined"]
        return date_joined
