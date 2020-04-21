from django.views import View
from django.forms import Form
from django.views.generic import TemplateView
from django.shortcuts import render, reverse, render_to_response
import traceback, os
from hello.form import UserForm
from hello.models import User


# def form_invalid(self, form):
#     """
#     If the form is invalid, re-render the context data with the
#     data-filled form and errors.
#     """
#     return self.render_to_response(self.get_context_data(form=form))


# def form_valid(self, form):
#     """
#     If the form is valid, redirect to the supplied URL.
#     """
#     return HttpResponseRedirect(self.get_success_url())

class UserListFormView(View):
    model = User

    def get(self, request): #请求到来时，返回用户主页
        users = User.objects.all()
        return render(request, 'hello/userlist.html', {"users": users})

    def get_context_data(self, **kwargs): #获取数据库数据，同主页一同返回
        print(kwargs)
        # print(UserForm.__dict__)
        context = super(UserListFormView, self).get_context_data(**kwargs)
        context["users"] = User.objects.filter(**kwargs)
        return context

    def post(self, request): #用户姓名搜索框
        keyword = request.POST.get("keyword", "")
        users = User.objects.all()
        if keyword:
            users = users.filter(name__icontains=keyword)
        return render(request, 'hello/userlist.html', {"users": users, "keyword": keyword})


class UserAddFormView(View):
    def get(self, request): #请求到来，返回页面
        return render(request, 'hello/useradd.html')

    def post(self, request): #数据提交，提交前会进行表单验证，通过后才会提交给后端
        form = UserForm(request.POST)
        print("表单已验证，即将判断表单是否合法~")
        if form.is_valid():
            print("表单验证通过")
            User.objects.create(**request.POST.dict())
            return render(request, 'hello/userlist.html', {"users": User.objects.all()})
        else:
            print("表单不合法，用户添加失败！")
            # return render(request, 'hello/useradd.html', {"form": form})
            return render_to_response('hello/useradd.html', {"form": form})


class UserDelFormView(TemplateView):
    template_name = 'hello/userdel.html'

    def get_context_data(self, **kwargs):
        user = User.objects.filter(pk=kwargs['pk'])
        context = super(UserDelFormView, self).get_context_data(**kwargs)
        context["user"] = user
        return context

    def post(self, request, **kwargs):
        users = User.objects.all()
        msg = {}
        form = UserForm(request.POST)
        print(form)
        try:
            if request.POST.get("delete") == "True": #接收前端返回值，True才删除
                User.objects.get(pk=kwargs['pk']).delete()
                msg = {"code": 0, "result": "删除成功"}
                return render(request, 'hello/userlist.html', {"users": users, "msg": msg})
            elif request.POST.get("delete") == "False":
                msg = {"code": 1, "result": "删除取消"}
                return render(request, 'hello/userlist.html', {"users": users, "msg": msg})
        except Exception as e:
            msg = {"code": 2, "errmsg": "删除失败，删除过程异常或用户不存在"}
        return render(request, 'hello/userdel.html', {"user": kwargs.get('pk'), "msg": msg})

class UserModFormView(TemplateView):
    field = ('name', 'password', 'age', 'sex')
    template_name = 'hello/usermod.html'

    def get_context_data(self, **kwargs):
        user = User.objects.filter(pk=kwargs['pk'])
        context = super(UserModFormView, self).get_context_data(**kwargs)
        context["user"] = user
        return context

    def post(self, request, **kwargs): #表单验证，验证无误后提交更新
        form = UserForm(request.POST)
        try:
            if form.is_valid():
                data = request.POST.dict()
                user = User.objects.filter(pk=kwargs['pk'])
                user.update(**data)
                users = User.objects.all()
                msg = {"code": 0, "result": "用户更新成功"}
                return render(request, 'hello/userlist.html', {"users": users, "msg": msg})
            else:
                msg = {"code": 1, "errmsg": "更新信息格式错误！"}
                return render_to_response('hello/usermod.html', {"form": form, "msg": msg})
        except Exception as e:
            print(e)
            msg = {"code": 1, "errmsg": "用户更新失败！"}
        return render(request, 'hello/usermod.html', {"msg": msg})


# class UserFormView(TemplateView, View):
#     template_name = 'hello/test.html'
#
#     def post(self, request):
#         # print(request.POST)
#         form = UserForm(request.POST, request.FILES)
#         print("已进行表单验证")
#         if form.is_valid():
#             print("表单验证通过")
#             print(form.cleaned_data)
#             file = form.cleaned_data['file']
#             if file:
#                 with open(os.path.join('hello/upload', file.name), 'wb') as f:
#                     for line in file.chunks():
#                         f.write(line)
#         else:
#             print('表单验证不通过')
#         return render(request, 'hello/test.html', {'form': form})
