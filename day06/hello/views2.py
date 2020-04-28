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
from django.views.generic import ListView
from pure_pagination.mixins import PaginationMixin

from hello.models import Project_User

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
                    if request.POST.get('agree') == "on":
                        userForm.save()
                        res = {"code": 0, "msg": "用户信息更新成功"}
                    else:
                        res = {"code": 4, "errmsg": "用户取消更新"}
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
    #     print("11111111111pk", kwargs)
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


class UserLoginJsView(TemplateView):
    template_name = 'dashboard/login.html'


class IndexJsView(TemplateView):
    template_name = 'dashboard/index.html'


# class TestListView(PaginationMixin, ListView):
#     # Important, this tells the ListView class we are paginating
#     template_name = 'hello/userlist.html'
#
#     model = Project_User
#     context_object_name = "users"
#     paginate_by = 3
#     # Replace it for your model or use the queryset attribute instead



# def page_not_found(request, exception, template_name='404.html'):
#     return render(request, template_name)

