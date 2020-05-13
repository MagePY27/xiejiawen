import logging
import traceback
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponse, render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.views.generic.base import View, TemplateView
from django.views.generic import DetailView
from django.contrib.auth.hashers import make_password, check_password
from .forms import LoginForm, PwdModForm
from users.models import UserProfile
from django.conf import settings

logger = logging.getLogger('UserProfile')
User = get_user_model()


# Create your views here.
class LoginView(View):
    """
    登录
    """
    def get(self, request):
        login_form = LoginForm()
        return render(request, "accounts/login.html", {'login_form': login_form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            print("form:", form)
            user = authenticate(request, username=username, password=password)
            print("user:", user, type(user))
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('users:index'))
                else:
                    return render(request, 'accounts/login.html', {'form': form, 'msg': '用户未激活！'})
            else:
                return render(request, 'accounts/login.html', {'form': form, 'msg': '用户名或密码错误！'})
        else:
            print("error:", form.errors())
            return render(request, 'accounts/login.html', {'form': form})


class LogoutView(View):
    """
    用户退出
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("accounts:login"))


class UserPwdView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'accounts/pwdmod.html'
    context_object_name = "user"
    redirect_field_name = None

    def post(self, request, **kwargs):
        pk = kwargs['pk']
        user = UserProfile.objects.get(pk=pk)
        print("pk:", pk)
        old_password_str = user.password
        pwdform = PwdModForm(request.POST, instance=user)
        print("old_str:", old_password_str, "old_pwd:", user.password)
        if not pk:
            res = {"code": 1, "errmsg": "用户不存在"}
            return render(request, settings.JUMP_PAGE, res)
        else:
            try:
                if pwdform.is_valid():
                    # 校验密码是否正确两次make_password不一致，因此需要使用check_password
                    is_correct = check_password(request.POST['password'], old_password_str)
                    print(is_correct)
                    if is_correct:
                        if request.POST.get('agree') == 'on':
                            user.password = request.POST['password_new']
                            user.save()
                            res = {"code": 0, "msg": "密码修改成功"}
                        else:
                            res = {"code": 2, "errmsg": "用户信息填写不完整或用户取消"}
                    else:
                        res = {"code": 5, "errmsg": "旧密码校验错误"}
                else:
                    # 获取表单的数据，便于排错
                    print(pwdform.errors)
                    print(pwdform.errors.as_json())
                    res = {"code": 3, "errmsg": pwdform.errors}
            except:
                # 获取更新操作的错误信息
                logger.error("modefy user error %s" % traceback.format_exc())
                res = {"code": 4, "errmsg": "密码修改失败"}
        return render(request, settings.JUMP_PAGE, res)


class UserPermModView(TemplateView):
    template_name = 'accounts/permmod.html'

