import logging
import traceback
import datetime
from django.shortcuts import render, reverse, Http404
from django.http import JsonResponse, QueryDict
from django.views.generic import ListView, TemplateView, DetailView
from django.db.models import Q, F
from hello.models import Project_User
from django.conf import settings
from hello.form import UserCreateForm, UserModefyForm

logger = logging.getLogger('Project_User')

class UserListJsView(ListView):
    """
    1.用户列表，可搜索姓名手机号
    """
    template_name = 'hello/userlist.html'
    model = Project_User
    context_object_name = "users"
    keyword = ""

    def get_queryset(self):
        """关键词搜索，姓名，手机号"""
        queryset = super(UserListJsView, self).get_queryset()
        self.keyword = self.request.GET.get("keyword", "").strip()
        if self.keyword:
            queryset = queryset.filter(Q(name__icontains=self.keyword) | Q(phone__icontains=self.keyword))
        return queryset

    def get_context_data(self, **kwargs):
        """将关键字保持在搜索框内, 将过滤后的数据传给前端"""
        context = super(UserListJsView, self).get_context_data(**kwargs)
        context["users"] = Project_User.objects.filter(**kwargs)
        return context

    def post(self, request):
        """创建用户"""
        userForm = UserCreateForm(request.POST)
        print(userForm)

        if userForm.is_valid():
            try:
                userForm.save()
                res = {"code": 0, "result": "用户创建成功"}
            except:
                logger.error("create user error: %s" % traceback.format_exc())
                res = {"code": 1, "errmsg": "用户创建失败"}
        else:
            # 获取表单数据
            print(userForm.errors)
            print(userForm.errors.as_json())
            res = {"code": 2, "errmsg": "表单不合法"}
        return render(request, settings.JUMP_PAGE, res)


class UserAddJsView(TemplateView):
    template_name = 'hello/useradd.html'

class UserDelJsView(TemplateView):
    template_name = 'hello/userdel.html'

    def post(self, request, **kwargs):
        # 先获取前端传过来的主键
        pk = Project_User.objects.filter(pk=kwargs['pk'])
        # 如果主键不存在，报用户不存在
        if not pk:
            res = {"code": 3, "errmsg": "用户不存在"}
            return render(request, settings.JUMP_PAGE, res)
        else:
            if request.POST.get('delete') == 'True':
                try:
                    Project_User.objects.filter(pk=pk).delete()
                    res = {"code": 0, "result": "用户删除成功"}
                except:
                    logger.error("delete user error %s" % traceback.format_exc())
                    res = {"code": 1, "errmsg": "用户删除异常"}
            elif request.POST.get('delete') == 'False':
                res = {"code": 2, "errmsg": "用户取消了删除操作"}
            else:
                res = {"code": 4, "errmsg": "其他异常"}
        return render(request, settings.JUMP_PAGE, res)


class UserModJsView(DetailView):
    """
    更新用户信息
    1.基于原信息修改，密码必须修改
    """
    model = Project_User
    template_name = 'hello/usermod.html'
    context_object_name = "user"

    def post(self, request, **kwargs):
        pk = Project_User.objects.filter(pk=kwargs['pk'])
        user = self.model.objects.filter(pk=pk)
        userForm = UserModefyForm(request.POST, instance=user)
        if not pk:
            res = {"code": 1, "errmsg": "用户不存在"}
            return render(request, settings.JUMP_PAGE, res)
        else:
            try:
                if userForm.is_valid():
                    userForm.save()
                    res = {"code": 0, "result": "用户信息更新成功"}
                else:
                    # 获取表单的数据，便于排错
                    print(userForm.errors)
                    print(userForm.errors.as_json())
                    res = {"code": 2, "errmsg": "表单不合法"}
            except:
                # 获取更新操作的错误信息
                logger.error("modefy user error %s"% traceback.format_exc())
                res = {"code": 3, "errmsg": "用户信息更新失败"}
        return render(request, settings.JUMP_PAGE, res)


class UserLoginJsView(TemplateView):
    template_name = 'dashboard/login.html'


class IndexJsView(TemplateView):
    template_name = 'dashboard/index.html'


def page_not_found(request, exception, template_name='404.html'):
    return render(request, template_name)
