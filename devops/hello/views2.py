from django.http import HttpRequest
from django.views.generic import View, ListView, TemplateView, CreateView, UpdateView, DeleteView
from hello.models import User
from django.shortcuts import reverse, render


class UserListView(View):
    model = User
    users = User.objects.all()

    def get(self, request):
        return render(request, 'hello/userlist.html', {"users":User.objects.all()})

    def post(self, request):
        # print(request.POST)
        keyword = request.POST.get('keyword')
        user_list = User.objects.filter(username__contains=keyword)

        return render(request, 'hello/userlist.html', {
            "keyword": keyword,
            "users_list": user_list,
        })

class UserAddView(View):
    def get(self, request):
        print(request.GET)
        return render(request, 'hello/useradd.html')

    def post(self, request):
        print(request.POST.dict())
        # msg = {}
        try:
            User.objects.create(**request.POST.dict())
            msg = {"code": 0, "result": "用户添加成功"}
        except:
            msg = {"code": 1, "errmsg": "用户添加失败：%s" % traceback.format_exc()}
        return render(request, 'hello/useradd.html', {
            "msg": msg,
        })

class UserDelView(View):
    def get(self,request, **kwargs):
        try:
            user = users.objects.get(id=kwargs['pk'])
            msg = {}
        except:
            msg = {"code": 1, "errmsg": "用户不存在: %s" % traceback.format_exc()}
        return render(request, 'hello/userdel.html', {"user": user, "msg":msg})


    def post(self,request, **kwargs):
        try:
            user = users.objects.get(id=kwargs['pk'])
            user.delete()
            msg = {"code":0, "result":"删除用户成功"}
        except:
            msg = {"code": 1, "errmsg": "删除用户失败: %s" % traceback.format_exc()}
        return render(request, 'hello/userdel.html', {"user":user, "msg":msg})


class UserModView(View):
    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        user = users.objects.get(id=pk)
        print(user.username, user.password, user.sex)
        return render(request, 'hello/useredit.html', {'user': user})


    def post(self, request, **kwargs):
        try:
            users.objects.filter(id=kwargs['pk']).update(**request.POST.dict())
            msg = {"code": 0, "result": "更新用户成功"}
            user = users.objects.get(id=kwargs['pk'])
        except:
            msg = {"code": 1, "errmsg": "更新用户失败: %s" % traceback.format_exc()}
        return render(request, 'hello/useredit.html', {"msg": msg, "user": user})