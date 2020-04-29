import logging
import traceback
import datetime
from django.shortcuts import render, reverse, Http404
from django.http import JsonResponse, QueryDict
from django.views.generic import View, ListView, TemplateView, DetailView
from django.db.models import Q, F
from hello.models import Project_User
from django.conf import settings
from hello.form import UserLoginForm, UserCreateForm, UserModefyForm
from django.views.generic import ListView
from pure_pagination.mixins import PaginationMixin

from hello.models import Project_User
from django.contrib.auth import authenticate, login, logout

logger = logging.getLogger('Project_User')


class UserListJsView(PaginationMixin, ListView):
    """
    1.用户列表，可搜索姓名手机号
    """
    template_name = 'hello/userlist.html'
    model = Project_User
    context_object_name = "users"
    paginate_by = 10

    # def get_queryset(self):
    #     """关键词搜索，姓名，手机号"""
    #     queryset = super(UserListJsView, self).get_queryset()
    #     self.keyword = self.request.GET.get("keyword", "").strip()
    #     if self.keyword:
    #         queryset = queryset.filter(Q(name__icontains=self.keyword) | Q(phone__icontains=self.keyword))
    #     return queryset

    # def get_context_data(self, **kwargs):
    #     """将关键字保持在搜索框内, 将过滤后的数据传给前端"""
    #     context = super(UserListJsView, self).get_context_data(**kwargs)
    #     context["users"] = Project_User.objects.filter(**kwargs)
    #     return context



    def post(self, request):
        """
        创建用户: 此功能使用表单来操作数据
        """
        print("POST:", request.POST)
        try:
            userForm = UserCreateForm(request.POST)
        except:
            res = {"code": 3, "errmsg": "信息填写不完整"}
            return render(request, settings.JUMP_PAGE, res)

        if userForm.is_valid():
            try:
                if request.POST.get('agree') == "on":
                    userForm.save()
                    res = {"code": 0, "msg": "用户创建成功"}
                    # 用户没有勾选同意按钮
                else:
                    res = {"code": 3, "errmsg": "信息填写不完整"}
            except:
                logger.error("create user error: %s" % traceback.format_exc())
                res = {"code": 1, "errmsg": "用户创建失败"}
        else:
            # 获取表单数据
            print(userForm.errors)
            # print(userForm.errors.as_json())
            res = {"code": 2, "errmsg": userForm.errors}
        return render(request, settings.JUMP_PAGE, res)


class UserAddJsView(TemplateView):
    template_name = 'hello/useradd.html'


class UserDelJsView(TemplateView):
    template_name = 'hello/userdel.html'

    def post(self, request, **kwargs):
        # 先获取前端传过来的主键
        pk=kwargs['pk']
        # 如果主键不存在，报用户不存在
        print(request.POST.get('comment'))
        if not pk:
            res = {"code": 3, "errmsg": "用户不存在"}
            return render(request, settings.JUMP_PAGE, res)
        else:
            if request.POST.get('comment') == "我确认":
                try:
                    Project_User.objects.filter(pk=pk).delete()
                    res = {"code": 0, "msg": "用户删除成功"}
                except:
                    logger.error("delete user error %s" % traceback.format_exc())
                    res = {"code": 1, "errmsg": "用户删除异常"}
            else:
                res = {"code": 2, "errmsg": "用户输入内容不满足要求，删除取消！"}
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
        print(request.POST, kwargs)
        pk = kwargs["pk"]
        user = Project_User.objects.get(pk=pk)
        userForm = UserModefyForm(request.POST, instance=user)
        if not pk:
            res = {"code": 1, "errmsg": "用户不存在"}
            return render(request, settings.JUMP_PAGE, res)
        else:
            try:
                print("userForm2:", userForm)
                if userForm.is_valid():
                    # 修改完后必须得勾选确认按钮，此功能应该在前端校验
                    if request.POST.get('agree') == "on":
                        userForm.save()
                        res = {"code": 0, "msg": "用户信息更新成功"}
                    else:
                        res = {"code": 4, "errmsg": "信息填写不完整"}
                else:
                    # 获取表单的数据，便于排错
                    print(userForm.errors)
                    print(userForm.errors.as_json())
                    res = {"code": 2, "errmsg": userForm.errors}
            except:
                # 获取更新操作的错误信息
                logger.error("modefy user error %s"% traceback.format_exc())
                res = {"code": 3, "errmsg": "用户信息更新失败"}
        return render(request, settings.JUMP_PAGE, res)

    # def post(self, request, **kwargs):
    #     pk = kwargs['pk']
    #     if not pk:
    #         res = {"code": 1, "errmsg": "用户不存在"}
    #     else:
    #         try:
    #             data = request.POST.dict()
    #             print("data:", data)
    #             if data["agree"] == "on":
    #                 data = data.pop('agree').pop('confirm_password')
    #                 User.objects.filter(pk=pk).update(**data)
    #                 res = {"code": 0, "errmsg": "用户信息更新成功"}
    #             else:
    #                 res = {"code": 2 , "errmsg": "用户取消更新操作"}
    #         except:
    #             logger.error("更新过程出现异常%s" % traceback.format_exc())
    #             res = {"code": 3, "errmsg": "更新异常"}
    #     return render(request, settings.JUMP_PAGE, res)


class UserLoginJsView(View):
    """
    登录验证：
    from django.contrib.auth.mixins import LoginRequiredMixin
    from django.contrib.auth import authenticate, login, logout
    """
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'dashboard/login.html')

    def post(self, request):
        print("POST:", request.POST)
        login_form = UserLoginForm(request.POST)
        print(login_form)
        ret = dict(login_form=login_form)
        if login_form.is_valid():
            name_input = request.POST["name"]
            password_input = request.POST["password"]
            data = Project_User.objects.filter(name=name_input, password=password_input)
            if data:
                ret["msg"] = "登录成功"
                data_list = list(data.values())
                pk = data_list[0]["id"]
                user = Project_User.objects.filter(pk=pk)
                return render(request, 'dashboard/index.html', {"user": user})
            else:
                ret["errmsg"] = "用户名或密码错误"
        else:
            ret["errmsg"] = "用户名和密码不能为空"
        return render(request, 'dashboard/login.html', ret)


    """
    使用Django自带的auth模块来校验登录
    """
    # def post(self, request, **kwargs):
    #     print("POST:", request.POST)
    #     # 此处先获取用户登录表单
    #     login_form = UserLoginForm(request.POST)
    #     # 将表单内容字典化，以便得会加入其它字段
    #     ret = dict(login_form=login_form)
    #     if login_form.is_valid():
    #         # 获取用户输入的用户名和密码
    #         name_input = request.POST["name"]
    #         password_input = request.POST["password"]
    #         user = authenticate(name=name_input, password=password_input)
    #         if user is not None:
    #             login(request, user)
    #             return render(request, 'dashboard/index.html')
    #         else:
    #             ret["errmsg"] = "用户名或密码错误"
    #     else:
    #         ret["errmsg"] = "用户名或密码不能为空"
    #     return render(request, 'dashboard/login.html', ret)


class IndexJsView(DetailView):
    template_name = 'dashboard/index.html'
    model = Project_User
    context_object_name = "user"
    # context_object_name = "user"
    #
    # def post(self, request, **kwargs):
    #     print("POST:", request.POST)
    #     pk = kwargs["pk"]
    #     user = Project_User.objects.filter(pk=pk)
    #     return render(request, 'dashboard/index.html')


class UserInfoJsview(DetailView):
    template_name = 'hello/userinfo.html'
    model = Project_User
    context_object_name = "user"

    def get(self,request, **kwargs):
        print("POST:", request.POST)
        pk = kwargs["pk"]
        user = Project_User.objects.filter(pk=pk)
        return render(request, 'hello/userinfo.html', {"user": user})

# class TestListView(PaginationMixin, ListView):
#     # Important, this tells the ListView class we are paginating
#     template_name = 'hello/userlist.html'
#
#     model = Project_User
#     context_object_name = "users"
#     paginate_by = 3
#     # Replace it for your model or use the queryset attribute instead


def page_not_found(request, exception, template_name='404.html'):
    return render(request, template_name)

