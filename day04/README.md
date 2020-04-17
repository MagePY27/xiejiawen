```
功能：
1.用户的增删改查
2.前端表单验证
3.基于用户名搜索
```
### 路由
**主路由**
```python
from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', include('hello.urls')),
]
```
**子路由**
```python
from django.urls import path, re_path
from hello import views, views2

app_name='hello'
urlpatterns = [
    path('', views.index, name='index'),
    # path('formview/', views2.UserFormView.as_view(), name='formview'),
    path('userlistformview/', views2.UserListFormView.as_view(), name='userlistFormview'),
    path('useraddformview/', views2.UserAddFormView.as_view(), name='useraddFormview'),
    re_path('userdelformview/(?P<pk>[0-9]+)?', views2.UserDelFormView.as_view(), name='userdelFormview'),
    re_path('usermodformview/(?P<pk>[0-9]+)?', views2.UserModFormView.as_view(), name='usermodFormview'),
]
```

### 表单验证函数
**基础设定**
```
hello/form.py,前半部分
```
```python
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

class UserForm(forms.Form):
    name = forms.CharField(max_length=12, required=True)
    password = forms.CharField(min_length=8,  max_length=16, required=True)
    # phone = forms.CharField(max_length=11, required=False)
    age = forms.IntegerField(max_value=100, required=False) #非必填，最大值为100
    sex = forms.IntegerField(required=False)
```

**表单验证**
```
hello/form.py,后半部分
```
```python
   def clean_name(self): #验证姓名的输入，长度<12并且必填
        name = self.cleaned_data['name']
        print(self.cleaned_data)
        num_name = len(name.strip())
        if not name:
            raise forms.ValidationError('name is Required Field!')
        if num_name > 12:
            raise forms.ValidationError('name is too long')
        return name

    def clean_password(self): #验证密码，必填，8<长度<16
        password = self.cleaned_data['password']
        num_password = len(password.strip())
        if not password:
            raise forms.ValidationError('password is Required Field!')
        if num_password < 8 or num_password >16:
            raise forms.ValidationError('password is longer than 16 or shorter than 8')
        # return "密码长度为:{}".format(password)
        return password

    def clean_age(self): #年龄，[0~100]
        age = self.cleaned_data['age']
        if not age:
            age=18
        elif int(age) > 100 or int(age) < 0:
                raise forms.ValidationError('invalid age format!')
        # return "年龄为:{}".format(age)
        return age

    def clean_sex(self): #无特殊要求，得是整数
        sex = self.cleaned_data['sex']
        return sex
```

### 用户功能部分

#### 用户功能后端
**环境部分**
```python
from django.views import View
from django.forms import Form
from django.views.generic import TemplateView
from django.shortcuts import render, reverse, render_to_response
import traceback, os
from hello.form import UserForm
from hello.models import User
```

**用户首页**
```python
class UserListFormView(View):
    model = User

    def get(self, request): #收到路由到的请求后，返回用户主页面
        users = User.objects.all()
        return render(request, 'hello/userlist.html', {"users": users})

    def get_context_data(self, **kwargs): #获取数据，传参到users，同主页面一起传给后端
        print(kwargs)
        # print(UserForm.__dict__)
        context = super(UserListFormView, self).get_context_data(**kwargs)
        context["users"] = User.objects.filter(**kwargs)
        return context

    def post(self, request): #基于用户名搜索
        keyword = request.POST.get("keyword", "")
        users = User.objects.all()
        if keyword:
            users = users.filter(name__icontains=keyword)
        return render(request, 'hello/userlist.html', {"users": users, "keyword": keyword})
```

**用户增加**
```表单数据需要校验```
```python
class UserAddFormView(View):
    def get(self, request):
        return render(request, 'hello/useradd.html')

    def post(self, request):
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
```
**用户删除**
```python
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
            if request.POST.get("delete") == "True":
                User.objects.get(pk=kwargs['pk']).delete() #获取数据和前端返回的确认值，然后删除
                msg = {"code": 0, "result": "删除成功"}
                return render(request, 'hello/userlist.html', {"users": users, "msg": msg})
            elif request.POST.get("delete") == "False":
                msg = {"code": 1, "result": "删除取消"}
                return render(request, 'hello/userlist.html', {"users": users, "msg": msg})
        except Exception as e:
            msg = {"code": 2, "errmsg": "删除失败，删除过程异常或用户不存在"}
        return render(request, 'hello/userdel.html', {"user": kwargs.get('pk'), "msg": msg})
```

**用户编辑**
```包含表单验证```
```python
class UserModFormView(TemplateView):
    field = ('name', 'password', 'age', 'sex')
    template_name = 'hello/usermod.html'

    def get_context_data(self, **kwargs): #获取用户数据传给前端，在修改时先显示原信息（好像并没有生效，不知道为啥）
        user = User.objects.filter(pk=kwargs['pk'])
        context = super(UserModFormView, self).get_context_data(**kwargs)
        context["user"] = user
        return context

    def post(self, request, **kwargs):
        form = UserForm(request.POST)
        try:
            if form.is_valid():
                data = request.POST.dict() #获取表单信息
                user = User.objects.filter(pk=kwargs['pk'])#解构信息
                user.update(**data) #基于新的用户信息进行修改
                users = User.objects.all()
                msg = {"code": 0, "result": "用户更新成功"}
                return render(request, 'hello/userlist.html', {"users": users, "msg": msg})
            else:
                msg = {"code": 1, "errmsg": "更新信息格式错误！"}
                #表单验证失败时，返回原页面，并返回表单错误信息
                return render_to_response('hello/usermod.html', {"form": form, "msg": msg})
        except Exception as e:
            print(e)
            msg = {"code": 1, "errmsg": "用户更新失败！"}
        #默认返回用户修改页面
        return render(request, 'hello/usermod.html', {"msg": msg})
```

### 前端
**用户首页**
```
hello/templates/userlist.html
前端页面中要输出表单的错误信息，不然前端格式有问题也不知道哪里出错了
```
```html
<html>
<body>
{% extends "base.html" %}
{% block title %} 用户管理系统
{% endblock %}


{% block content %}
{% if msg.code == 0 %}
    <p style="color:green">{{ msg.result }}</p>
{% else %}
    <p style="color:red">{{ msg.errmsg }}</p>
{% endif %}

 {% if form %}
     {{ form.errors }} <!--此处的表单错误信息很重要，用户显示表单的错误信息 -->
 {% endif %}

<a href="{% url 'hello:userlistFormview' %}">主页 </a>
<a href="{% url 'hello:useraddFormview' %}">新增用户</a>
<br>
<br>

<form method="post" action="" enctype="multipart/form-data">
<!--    #方法为post，后端接收-->
    <input type="text" name="keyword" value="{{ keyword }}" placeholder="请输入关键字~">
    <button type="submit">搜索</button>
</form>

<table border="1">
<thead>
    <tr>
        <th>ID</th>
        <th>姓名</th>
        <th>密码</th>
        <th>年龄</th>
        <th>性别</th>
        <th>管理</th>
    </tr>
</thead>
<tbody>
    {% for user in users %}
    <tr>
        <td>{{ user.id }}</td>
        <td>{{ user.name }}</td>
        <td>{{ user.password }}</td>
        <td>{{ user.age }}</td>
        <td>{% if user.sex == 0 %}男 {% elif user.sex == 1 %}女 {% else %}保密 {% endif %}</td>
        <td><a href="{% url 'hello:usermodFormview' user.id %}">编辑</a>  <a href="{% url 'hello:userdelFormview' user.id %}">删除</a></td>
<!--        传参给后端页面， 用户id： user.id这个也很重要，传给url，以便返回相应的url路径
-->
    </tr>
    {% endfor %}
</tbody>
</table>
{% endblock %}
</body>
</html>
```
**用户添加**
```没啥可说的，也需要添加表单错误输出代码```
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>用户添加</title>
</head>
<body>
{% extends "base.html" %}
{% block title %} 用户管理系统
{% endblock %}

{% block content %}
 {% if form %}
    {{ form.errors }}
 {% endif %}
<a href="{% url 'hello:userlistFormview' %}">返回</a>
{% if msg.code == 0 %}
    <p style="color:green">{{ msg.result }}</p>
{% else %}
    <p style="color:red">{{ msg.errmsg }}</p>
{% endif %}

<h4>新增用户：</h4>
<form action="" method="post" enctype="multipart/form-data">
name:<br>
<input type="text" name="name">
<br>
password:<br>
<input type="password" name="password">
<br>
age:<br>
<input type="text" name="age">
<br>
sex:<br>
<input type="radio" name="sex" value="0" checked>男
<input type="radio" name="sex" value="1">女
<input type="radio" name="sex" value="2">保密
<br><br>
<input type="submit" value="提交">
<input type="reset" value="重置">
</form>
<br>
{% endblock %}

</body>
</html>
```
**用户删除**
```包含表单错误信息的输出代码， form表单的delete变量值会传给后端，以便判断是否删除此用户```
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>用户删除</title>
</head>
<body>
{% extends "base.html" %}
{% block title %} 用户管理系统
{% endblock %}
{% block content %}
{% if msg.code == 0 %}
    <p style="color:green">{{ msg.result }}</p>
{% else %}
    <p style="color:red">{{ msg.errmsg }}</p>
{% endif %}
<h3>确定要删除吗？？</h3>
 {% if form %}
     {{ form.errors }}
 {% endif %}
<form method="post">
    <input type="radio" name="delete" value='True'>是<input type="radio" name="delete" value='False' checked>否
    <input type="submit" value="确认">
</form>
{% endblock %}
</body>
</html>
```
**用户编辑**
```表单验证，表单错误信息输出代码```
```html
{% extends 'base.html' %}
{% block title %}
    <p style="background-color: aqua">用户修改</p>
{% endblock %}


{% block content %}

 {% if form %}
     {{ form.errors }}
 {% endif %}

{% if msg.code == 0 %}
    <p style="color:green">{{ msg.result }}</p>
{% else %}
    <p style="color:red">{{ msg.errmsg }}</p>
{% endif %}

<h2><a href="{% url 'hello:userlistFormview' %}">返回 </a></h2>

    <form  method="post" action="" enctype="multipart/form-data">
        姓名:<br>
        <input type="text" name="name" value={{ user.name }}><br>
        密码:<br>
        <input type="password" name="password" value={{ user.password }}><br>
        年龄:<br>
        <input type="text" name="age" value={{ user.age }}><br>
        性别:<br>
        {% if user.sex == 0 %}
        <input type="radio" name="sex" value=0 checked>女
        <input type="radio" name="sex" value=1 >男
        <input type="radio" name="sex" value=2>未知<br>
        {% elif user.sex == 1 %}
        <input type="radio" name="sex" value=0 >女
        <input type="radio" name="sex" value=1 checked>男
        <input type="radio" name="sex" value=2>未知<br>
        {% else %}
        <input type="radio" name="sex" value=1>男
        <input type="radio" name="sex" value=0>女
        <input type="radio" name="sex" value=2 checked>未知<br>
        {% endif %}
        <input type="submit" value="提交">
    </form>
{% endblock %}
```