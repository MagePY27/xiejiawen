import logging
import traceback
import datetime
from django.shortcuts import render, reverse, Http404, HttpResponseRedirect, get_object_or_404
from django.http import JsonResponse, QueryDict
from django.views.generic import View, ListView, TemplateView, DetailView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q, F
from django.conf import settings
from users.form import UserLoginForm, UserCreateForm, UserModefyForm
from django.views.generic import ListView, UpdateView, DeleteView
from pure_pagination.mixins import PaginationMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from users.models import UserProfile
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse, reverse_lazy

logger = logging.getLogger('UserProfile')
User = get_user_model()


class IndexView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    登录功能
    """
    # 用户没有通过时跳转的地址，默认是 settings.LOGIN_URL.
    # 在settings中设置LOGIN_URL='/accounts/login/'
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    redirect_field_name = None
    permission_required = 'users.view_userprofile'

    def get(self, request):
        # print(request.user)
        # print(request.user.is_authenticated)
        # if not request.user.is_authenticated:
        #     return HttpResponseRedirect(reverse("accounts:login"))
        return render(request, 'index.html')

    def post(self, request):
        return render(request, 'index.html')


class UserListJsView(LoginRequiredMixin, PermissionRequiredMixin, PaginationMixin,  ListView):
    """
    1.用户列表，可搜索姓名手机号
    """

    template_name = 'users/userlist.html'
    model = UserProfile
    context_object_name = "users"
    paginate_by = 5
    permission_required = 'users.view_userprofile'

    # 用户没有通过时跳转的地址，默认是 settings.LOGIN_URL.
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    # redirect_field_name = None
    keyword = ""

    # 数据过滤
    def get_queryset(self):
        queryset = super(UserListJsView, self).get_queryset()
        queryset = queryset.exclude(username='admin')
        self.keyword = self.request.GET.get("keyword", "")
        if self.keyword:
            queryset = queryset.filter(Q(name__icontains=self.keyword) |
                                       Q(username__icontains=self.keyword) |
                                       Q(phone__icontains=self.keyword))

        return queryset

    # 搜索关键字传给前端
    def get_context_data(self, **kwargs):
        context = super(UserListJsView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context

    def post(self, request):
        """
        创建用户: 此功能使用表单来操作数据
        """
        print("POST:", request.POST)
        try:
            userForm = UserCreateForm(request.POST)
            print(type(userForm))
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


class UserAddJsView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    # 用户没有通过时跳转的地址，默认是 settings.LOGIN_URL.
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    redirect_field_name = None
    template_name = 'users/useradd.html'
    permission_required = 'users.add_userprofile'


class UserDelJsView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    # 用户没有通过时跳转的地址，默认是 settings.LOGIN_URL.
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    redirect_field_name = None
    template_name = 'users/userdel.html'
    permission_required = 'users.delete_userprofile'

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
                    UserProfile.objects.filter(pk=pk).delete()
                    res = {"code": 0, "msg": "用户删除成功"}
                except:
                    logger.error("delete user error %s" % traceback.format_exc())
                    res = {"code": 1, "errmsg": "用户删除异常"}
            else:
                res = {"code": 2, "errmsg": "用户输入内容不满足要求，删除取消！"}
        return render(request, settings.JUMP_PAGE, res)


class UserModJsView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DetailView):
    """
    更新用户信息
    1.基于原信息修改，密码必须修改
    """
    model = UserProfile
    template_name = 'users/usermod.html'
    # context_object_name = "user"
    permission_required = 'users.change_userprofile'
    # 用户没有通过时跳转的地址，默认是 settings.LOGIN_URL.
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    # redirect_field_name = None

    def post(self, request, **kwargs):
        print(request.POST, kwargs)
        pk = kwargs["pk"]
        data = request.POST.dict()
        user = UserProfile.objects.get(pk=pk)
        # instance指定用户，否则会新建
        # 密码会在models中加密然后入库
        userForm = UserModefyForm(request.POST, instance=user)
        if not pk:
            res = {"code": 1, "errmsg": "用户不存在"}
            return render(request, settings.JUMP_PAGE, res)
        else:
            try:
                # print("userForm2:", userForm)
                if userForm.is_valid():
                    # 修改完后必须得勾选确认按钮，此功能应该在前端校验
                    if request.POST.get('agree') == "on":
                        userForm.save(commit=True)
                        # data.pop('agree')
                        # data.pop('csrfmiddlewaretoken')
                        # self.model.objects.filter(pk=pk).update(**data)
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


class UserInfoJsView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    template_name = 'users/userinfo.html'
    model = UserProfile
    context_object_name = "user"
    permission_required = 'users.view_userprofile'
    # 用户没有通过时跳转的地址，默认是 settings.LOGIN_URL.
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    redirect_field_name = None

    def get(self, request, **kwargs):
        print("POST:", request.POST)
        pk = kwargs["pk"]
        user = UserProfile.objects.filter(pk=pk)
        return render(request, 'users/userinfo.html', {"user": user})


class GroupListView(LoginRequiredMixin, PermissionRequiredMixin, PaginationMixin, ListView):
    # class GroupListView(LoginRequiredMixin, PaginationMixin, ListView):
    """
    组列表
    """
    template_name = 'users/grouplist.html'
    model = Group
    ordering = 'id'
    paginate_by = 5
    permission_required = 'auth.view_group'
    keyword = ""

    def get_keyword(self):
        self.keyword = self.request.GET.get('keyword')
        return self.keyword

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.get_keyword()
        if keyword:
            queryset = queryset.filter(name__icontains=keyword)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context


class GroupAddView(LoginRequiredMixin, PermissionRequiredMixin, PaginationMixin, CreateView):
    """
     添加组
    """
    template_name = 'users/groupadd.html'
    model = Group
    fields = ('name', 'permissions')
    success_message = '%(name)s 组添加成功！'
    permission_required = 'auth.add_group'

    def get_success_url(self):
        if '_addanother' in self.request.POST:
            return reverse('users:group_add')
        return reverse('users:group_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        permissions = Permission.objects.exclude(Q(content_type__model='session') |
                                                 Q(content_type__model='contenttype') |
                                                 Q(content_type__model='logentry') |
                                                 Q(codename='add_permission') |
                                                 Q(codename='delete_permission')
                                                 ).values('id', 'name',
                                                          'content_type__app_label',
                                                          'codename')
        context['permissions'] = permissions
        return context


class GroupAddUserView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, View):
    """
    批量将用户添加到组
    """
    permission_required = 'auth.add_group'

    def get(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        users = User.objects.all()
        context = {'group': group, 'users': users}
        return render(request, 'users/group_add_user.html', context=context)

    def post(self, request, pk):
        uids = request.POST.getlist('users')
        group = get_object_or_404(Group, pk=pk)
        if uids:
            users = User.objects.filter(id__in=uids)
            group.user_set.set(users)
        else:
            group.user_set.clear()
        messages.success(request, '{}组添加用户或移除用户成功！'.format(group))
        if '_addanother' in request.POST:
            return HttpResponseRedirect(reverse('users:group_add_user', kwargs={'pk': pk}))
        return HttpResponseRedirect(reverse('users:group_list'))


class GroupUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    更新组
    """
    template_name = 'users/group_update.html'
    model = Group
    fields = ('name', 'permissions')
    success_message = '%(name)s 组更新成功！'
    permission_required = 'auth.change_group'

    def get_success_url(self):
        if '_addanother' in self.request.POST:
            return reverse('users:group_add')
        elif '_savedit' in self.request.POST:
            return reverse('users:group_update', kwargs={'pk': self.kwargs['pk']})
        else:
            return reverse('users:group_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        permissions = Permission.objects.exclude(Q(content_type__model='session') |
                                                 Q(content_type__model='contenttype') |
                                                 Q(content_type__model='logentry') |
                                                 Q(codename='add_permission') |
                                                 Q(codename='delete_permission')
                                                 ).values('id', 'name',
                                                          'content_type__app_label',
                                                          'codename')
        context['permissions'] = permissions
        return context


class GroupDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    删除组
    """
    template_name = 'users/group_confirm_delete.html'
    model = Group
    permission_required = 'auth.delete_group'

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, '{} 组删除成功~'.format(self.object.name))
        return response

    def get_success_url(self):
        return reverse_lazy('users:group_list')


# class IndexJsView(DetailView):
#     template_name = 'dashboard/index.html'
#     model = UserProfile
#     context_object_name = "user"
#     #
#     # def post(self, request, **kwargs):
#     #     print("POST:", request.POST)
#     #     pk = kwargs["pk"]
#     #     user = UserProfile.objects.filter(pk=pk)
#     #     return render(request, 'dashboard/index.html')

# class TestListView(PaginationMixin, ListView):
#     # Important, this tells the ListView class we are paginating
#     template_name = 'users/userlist.html'
#
#     model = UserProfile
#     context_object_name = "users"
#     paginate_by = 3
#     # Replace it for your model or use the queryset attribute instead
# class UserLoginJsView(View):
#     """
#     登录验证：
#     from django.contrib.auth.mixins import LoginRequiredMixin
#     from django.contrib.auth import authenticate, login, logout
#     """
#     def get(self, request):
#         if not request.user.is_authenticated:
#             return render(request, 'dashboard/login.html')
#
#     def post(self, request):
#         print("POST:", request.POST)
#         login_form = UserLoginForm(request.POST)
#         print("form:", login_form)
#         ret = dict(login_form=login_form)
#         print("ret:", ret)
#         if login_form.is_valid():
#             username_input = request.POST["username"]
#             password_input = request.POST["password"]
#             data = UserProfile.objects.filter(username=username_input, password=password_input)
#             if data:
#                 ret["msg"] = "登录成功"
#                 data_list = list(data.values())
#                 pk = data_list[0]["id"]
#                 user = UserProfile.objects.filter(pk=pk)
#                 print("user:", user)
#                 return render(request, 'dashboard/index.html', {"user": user})
#             else:
#                 ret["errmsg"] = "账号或密码错误"
#         else:
#             print(login_form.errors)
#             ret["errmsg"] = "账号和密码不能为空"
#         return render(request, 'dashboard/login.html', ret)
#
#
#     """
#     使用Django自带的auth模块来校验登录
#     """
#     # def post(self, request, **kwargs):
#     #     print("POST:", request.POST)
#     #     # 此处先获取用户登录表单
#     #     login_form = UserLoginForm(request.POST)
#     #     # 将表单内容字典化，以便得会加入其它字段
#     #     ret = dict(login_form=login_form)
#     #     if login_form.is_valid():
#     #         # 获取用户输入的用户名和密码
#     #         name_input = request.POST["name"]
#     #         password_input = request.POST["password"]
#     #         user = authenticate(name=name_input, password=password_input)
#     #         if user is not None:
#     #             login(request, user)
#     #             return render(request, 'dashboard/index.html')
#     #         else:
#     #             ret["errmsg"] = "用户名或密码错误"
#     #     else:
#     #         ret["errmsg"] = "用户名或密码不能为空"
#     #     return render(request, 'dashboard/login.html', ret)
