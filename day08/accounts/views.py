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
from django.views.generic import DetailView, ListView, UpdateView
from django.contrib.auth.hashers import make_password, check_password
from .forms import LoginForm, PwdModForm
from users.models import UserProfile
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.db.models import Q, F
from pure_pagination.mixins import PaginationMixin
from django.contrib.contenttypes.models import ContentType

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
            # print("form:", form)
            print(request.POST)
            user = authenticate(request, username=username, password=password)
            print("user:", user, type(user))
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('users:index'))
                else:
                    # 用户未激活仍显示密码错误
                    return render(request, 'accounts/login.html', {'form': form, 'msg': '未激活！'})
            else:
                return render(request, 'accounts/login.html', {'form': form, 'msg': '用户名或密码错误！'})
        else:
            return render(request, 'accounts/login.html', {'form': form})


class LogoutView(View):
    """
    用户退出
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("accounts:login"))


class UserPwdView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'accounts/pwdmod.html'
    context_object_name = "user"
    redirect_field_name = None
    permission_required = 'users.change_userprofile'

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
                    # 校验密码是否正确,两次都使用make_password时会不一致，因此需要使用check_password
                    is_correct = check_password(request.POST['password'], old_password_str)
                    print(is_correct)
                    if is_correct:
                        if request.POST.get('change_password') == 'on':
                            # 加密密码， 然后入库
                            password_new = make_password(request.POST['password_new'], None, 'pbkdf2_sha256')
                            user.password = password_new
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


class PermListView(LoginRequiredMixin, PermissionRequiredMixin,PaginationMixin, ListView):
    template_name = 'accounts/permlist.html'
    model = Permission
    paginate_by = 4
    permission_required = 'auth.view_permission'
    keyword = None

    def get_query_term(self):
        self.keyword = self.request.GET.get('keyword', None)
        return self.keyword

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(content_type__model__in=['logentry', 'session', 'contenttype'])
        keyword = self.get_query_term()
        if keyword:
            queryset = queryset.filter(Q(name__icontains=keyword) | Q(content_type__app_label__icontains=keyword) |
                                       Q(codename__icontains=keyword))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context


class PermUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    更新权限
    """
    template_name = 'accounts/permupdate.html'
    model = Permission
    fields = ('name',)
    success_message = '%(name)s 重命名成功！'
    permission_required = 'auth.change_permission'

    def get_success_url(self):
        if '_addanother' in self.request.POST:
            return reverse('accounts:permlist')
        elif '_savedit' in self.request.POST:
            return reverse('accounts:permupdate', kwargs={'pk': self.object.pk})
        return reverse('accounts:permlist')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_types = ContentType.objects.all()
        context['content_types'] = content_types
        return context



