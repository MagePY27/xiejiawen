from django import forms
from django.contrib.auth import get_user_model
from users.models import UserProfile


User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(required=True, error_messages={'required': '用户名不能为空'})
    password = forms.CharField(required=True, error_messages={'required': '密码不能为空'})


class PwdModForm(forms.ModelForm):
    password_new = forms.CharField(required=True, error_messages={'required': '密码不能为空'})
    password_new_confirm = forms.CharField(required=True, error_messages={'required': '密码不能为空'})
    class Meta:
        model = UserProfile
        fields = ['password', 'password_new']

    def clean_password(self):
        if "password" not in self.cleaned_data.keys():
            raise forms.ValidationError("密码为必填项", code="ValueErr")
        else:
            password_old_input = self.cleaned_data['password']
            if len(password_old_input.strip()) < 8 or len(password_old_input.strip()) > 16:
                raise forms.ValidationError("你的密码太长或太短")
            else:
                return password_old_input

    def clean_password_new(self):
        if "password_new" not in self.cleaned_data.keys():
            raise forms.ValidationError("密码为必填项", code="ValueErr")
        else:
            password_new = self.cleaned_data['password_new']
            if len(password_new.strip()) < 8 or len(password_new.strip()) > 16:
                raise forms.ValidationError("你的密码太长或太短")
            else:
                return password_new

    def clean_passowrd_new_confirm(self):
        if "password_new" not in self.cleaned_data.keys():
            raise forms.ValidationError("password_new字段不合法", "ValueErr")
        else:
            password_new = self.cleaned_data["password_new"]
            # 首先判断密码是否非空
            if "password_new_confirm" not in self.cleaned_data.keys():
                raise forms.ValidationError("密码为必填项", code="ValueErr")
            else:
                password_new_confirm = self.cleaned_data["password_new_confirm"]
                if password_new_confirm != password_new:
                    raise forms.ValidationError("两次密码不一致", code="MismatchErr")
                # 两个字段相等才能到这一步，这一步直接判断password的长度即可，密码可能包含空格，因此不使用strip
                elif len(password_new) < 8 or len(password_new) > 16:
                    raise forms.ValidationError("密码太长或太短", code="invalid")
                else:
                    return password_new_confirm