from django.http import HttpRequest
from django.views.generic import View, ListView, TemplateView, CreateView, UpdateView, DeleteView
from hello.models import User
from django.shortcuts import reverse, render
import traceback


class UserListView(TemplateView, View):
    """
    用户列表
    用户姓名搜索
    """
    # def get(self, request):
    #     return render(request, 'hello/userlist.html', {"users": User.objects.all()})
    template_name = 'hello/userlist.html'
    # model = User
    def get_context_data(self, **kwargs):
        print(kwargs)
        data = super(UserListView, self).get_context_data(**kwargs)
        data["users"] = User.objects.filter(**kwargs) #传递users变量给userlist
        return data

    def post(self, request): #接收前端post的keyword来过滤
        keyword = request.POST.get("keyword", "")
        users = User.objects.all()
        if keyword:
            users = users.filter(name__icontains=keyword)
        return render(request, 'hello/userlist.html', {"users": users, "keyword": keyword})

class UserAddView(View):
    def get(self, request):
        return render(request, 'hello/useradd.html')

    def post(self, request):
        print(request.POST.dict())
        # msg = {}
        try:
            User.objects.create(**request.POST.dict())
            msg = {"code": 0, "result": "用户添加成功"}
            users = User.objects.all()
            return render(request, 'hello/userlist.html', {"users": users, "msg": msg})
        except:
            msg = {"code": 1, "errmsg": "用户添加失败：%s" % traceback.format_exc()}
        return render(request, 'hello/useradd.html', {
            "msg": msg,
        })

class UserDelView(TemplateView, View):
    # def get(self,request, **kwargs):
    #     try:
    #         # pk = kwargs.get('pk')
    #         msg = {}
    #     except:
    #         msg = {"code": 1, "errmsg": "用户不存在: %s" % traceback.format_exc()}
    #     return render(request, 'hello/userdel.html', {"pk": kwargs.get('pk'), "msg": msg})
    template_name = 'hello/userdel.html'

    def get_context_data(self, **kwargs):
        user = User.objects.filter(pk=kwargs['pk'])
        data = super(UserDelView, self).get_context_data(**kwargs)
        data["user"] = user
        return data

    def post(self,request, **kwargs):
        users = User.objects.all()
        try:
            if request.POST.get('delete') == "True":
                User.objects.get(pk=kwargs['pk']).delete()
                msg = {"code":0, "result":"删除用户成功"}
                return render(request, 'hello/userlist.html', {"users": users, "msg": msg})
            elif request.POST.get('delete') == "False":
                msg = {"code": 1, "result": "删除取消"}
                return render(request, 'hello/userlist.html', {"users": users, "msg": msg})
        except:
            msg = {"code": 1, "errmsg": "删除用户失败: %s" % traceback.format_exc()}
        return render(request, 'hello/userdel.html', {"user": kwargs.get('pk'), "msg": msg})


class UserModView(TemplateView, View):
    # def get(self, request, **kwargs):
    #     pk = kwargs.get('pk')
    #     user = User.objects.get(pk=kwargs.get('pk'))
    #     print(kwargs, pk, request)
    #     return render(request, 'hello/usermod.html', {"user": user})
    # model = User
    field = ('name', 'password', 'age', 'sex')
    template_name = 'hello/usermod.html'

    def get_context_data(self, **kwargs):
        print(kwargs)
        user = User.objects.filter(pk=kwargs['pk']) #需要前端传数据
        data = super(UserModView, self).get_context_data(**kwargs)
        data["user"] = user
        return data

    def post(self, request, **kwargs):
        try:
            User.objects.filter(pk=kwargs['pk']).update(**request.POST.dict())
            msg = {"code": 0, "result": "更新用户成功"}
            users = User.objects.all()
            return render(request, 'hello/userlist.html', {"msg": msg, "users": users})
            #修改成功返回至主页面
        except:
            msg = {"code": 1, "errmsg": "更新用户失败: %s" % traceback.format_exc()}
        return render(request, 'hello/usermod.html', {"msg": msg, "user": pk})