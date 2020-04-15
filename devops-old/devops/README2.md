```本文用于说明此项目用户的增删改查功能```
#### 主路由不变，修改子路由
```python
from django.urls import path, re_path
from . import views
app_name = 'hello'
urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.list, name='list'),
    path('userlist/', views.userlist, name = 'userlist'),#用户主列表包含搜索
    path('useradd/', views.useradd, name = 'useradd'), #用户添加
    re_path('userdel/(?P<user_id>[0-9]{1,})', views.userdel, name='userdel'), #用户删除，name命名空间
    re_path('usermod/(?P<user_id>[0-9]{1,})', views.usermod, name='usermodefy') #用户修改
]
```

#### 用户添加
**后端配置**
```python
def useradd(request):
     """
     添加用户：request获取表单提交的方式有多种
          1.request.POST.get()适用于获取单个变量进行处理的场景
          2.request.POST.dict()适用于将表单所有的数据整体进行处理
          3.Form(request.POST)适用于表单类验证的场景（生产中最常用）
          4.注意要导入各种需要的包
     """
     msg={}
     if request.method == "POST":
          try:
               print(request.POST)
               #方法一，参数逐个添加
               # name = request.POST.get('name', "")
               # password = request.POST.get('password', "")
               # age = request.POST.get('age', "")
               # sex = request.POST.get('sex', "")
               # u = User()
               # u.name = name
               # u.password = password
               # u.age = int(age)
               # u.sex = int(sex)
               # u.save()
               # msg = {'code': 0, "result": "用户添加成功"}
               # print(msg)
               # 方法二，使用参数解构
               data = request.POST.dict()
               User.objects.create(**data)
               msg = {'code': 0, "result": "用户添加成功"}
          except Exception as e:
               print(e)
               msg = {'code': 1, "errmsg": "添加用户失败: %s" % traceback.format_exc()} #
          finally:
               return render(request, 'hello/index.html', {"msg": msg, "users":User.objects.all()})
     return render(request, 'hello/useradd.html', {"msg": msg}) #第一步接收到修改请求时跳转此页面
```
**前端配置**
```html
# ~]$ cat devops/templates/hello/useradd.html核心内容
{% if msg %} #用户接收后端的返回信息
    {{msg}}<br>
{% endif %}
<b><a href="{% url 'hello:userlist' %}">返回</a></b>
    <form method="post" action="">
        姓名:
        <input type="text" name="name" >
        <br>
        密码:
        <input type="password" name="password">
        <!--密码框隐藏 -->
        <br>
        年龄:
        <input type="text" name="age">
        <br>
        性别:
        <!-- 性别的显示 男，女，未知 -->
            <input type="radio" name="sex" value=1 checked>男
            <input type="radio" name="sex" value=0>女
            <input type="radio" name="sex" value=2>未知
            <br>
        <button type="submit">确认</button>
    </form>
```
#### 用户删除
**前端页面**
```html
<b><a href="{% url 'hello:list' %}">返回</a></b>
{% if msg %}
    <h2>msg: {{msg.result}}, code: {{msg.code}}</h2><br> 
    <!--  -->
{% endif %}
<form  method="post">
    <b>删除用户{{user.user}}?</b><br>
<!--    <a href="/hello/userdel/{{user.id}}/delete=True">Yes</a>/<a href="/hello/userlist/">No</a>-->
    <input type="radio" name="delete" value='True'>是<input type="radio" name="delete" value='False' checked>否
    <input type="submit" value="确认">
</form>
```
**后端配置**
```python
def userdel(request, user_id):
     try:
          u = User.objects.get(id=user_id) #每次进入删除页面时判断用户是否存在
     except User.DoesNotExist:
          raise Http404("User does not exist") #对于不存在的用户返回404，或者删除之后再次刷新当前页面也会返回404
     msg = {}
     try:
          if u:
               if request.POST.get('delete') == 'True': #接收前端按钮返回的数据
                    u.delete() #直接删除
                    msg = {"result": '删除成功', "code": 0}
                    return render(request, 'hello/userdel.html', {"msg": msg, "users": User.objects.all()})
               elif request.POST.get('delete') == 'False':
                    msg = {"result": "删除取消", "code": 1}
                    return render(request, 'hello/index.html', {"msg":msg, "users": User.objects.all()}) #删除取消后返回主页面
               else:
                    return render(request, 'hello/userdel.html', {"user": u})
     except Exception as e:
          raise e
     return render(request, 'hello/userdel.html', {'msg': msg})
```

#### 用户修改
**前端页面**
```html
<b><a href="{% url 'hello:userlist' %}">返回</a></b>
<form method="post" action="">
    姓名:
    <input type="text" name="name" value={{ user.name }}> 
    <!-- 显示已有的信息，基于此信息进行修改 -->
    <br>
    密码:
    <input type="password" name="password" value={{ user.password }}>
    <br>
    年龄:
    <input type="text" name="age" value={{ user.age }}>
    <br>
    性别:
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
        <button type="submit">确认</button>
        <!-- 提交后，将各个字段的信息发送至后端，后端将参数进行解构并更新至数据库 -->
</form>
```
**后端数据**
```python
def usermod(request, user_id):
     try: #用户存在性检查
          m = User.objects.get(id=user_id)
          # user = get_object_or_404(id=user_id) #更简便地判断用户是否存在，不存在返回404，建议使用此方式
     except User.DoesNotExist:
          raise Http404("User does not Exist!") #提前需要导入Http404包
     if request.method == 'POST': #接受前端数据
          try:
               data = request.POST.dict()
               User.objects.filter(id=user_id).update(**data) #解析数据然后更新
               msg={'code': 0, 'result': '用户更新成功'}
               return render(request, 'hello/index.html', {'users': User.objects.all(), 'msg': msg}) 
               # 修改完成则自动返回用户页面
          except Exception as e:
               msg={'code': 1, 'result': '用户更新失败 %s' % traceback.format_exc()} #报错处理
               return render(request, 'hello/index.html', {'users': User.objects.all(), 'msg': msg}) 
               #修改失败则返回主页，并返回相应信息
     return render(request, 'hello/usermod.html', {'user': m}) #跳转至修改页面进行修改
```

#### 用户显示与搜索
**前端页面
```html
<body>
{% extends "base.html" %}
<!--
引用母版的题头和结尾
-->
{% block title %} 用户的列表  {% endblock %}
<!--
重写母版变的部分
-->
{% block content %}
<table border="1">
    <a href="{% url 'hello:userlist' %}">主页 </a>
    <a href="{% url 'hello:useradd' %}">用户添加</a><br> 
    <!--第一行就是显示两个按钮-->
{% if msg %}
    <h2>msg: {{msg.result}}, code: {{msg.code}}</h2><br> 
    <!--接收后端的返回数据并显示-->
{% endif %}
    <form action="">
        <input type="text" name="keyword" value="{{ keyword }}" placeholder="请输入关键字:">
        <!--value需要带引号，不然搜索框内容显示异常-->
        <button type="submit">搜索</button>
    </form>

<thead>
    <tr>
        <th>用户名 </th>
        <th>姓名 </th>
        <th>密码 </th>
        <th>年龄 </th>
        <th>性别 </th>
        <th>操作 </th>
    </tr>
</thead>
<tbody>
    {% for user in users %}
    <tr>
        <td>{{ user.id }}</td>
        <td>{{ user.name }}</td>
        <td>{{ user.password }}</td>
        <td>{{ user.age }}</td>
        <td>
            {% if user.sex == 0 %}女{% elif user.sex == 1 %}男{% else %}未知{% endif %}
            <!-- 对数据库中的数据进行转换，0表示女，1表示男，其他表示未知>
        </td>
        <!-- <td><a href="/hello/userdel/{{user.id}}" id="del_user">删除</a>-->
        <td>
            <a href="{% url 'hello:userdel' user.id %}">删除</a>
            <a href="{% url 'hello:usermodefy' user.id %}">修改</a>
        </td>
    </tr>
    {% endfor %}
</tbody>
</table>
{% endblock %}
</body>
```
**后端配置**
```python
def userlist(request):
     """
     1.用户列表
     2.姓名搜索功能
     # http://url/?keyword=aaa
     """
     keyword = request.GET.get("keyword", "")#接收输入的关键字
     print(keyword)
     users = User.objects.all()
     if keyword:
         users = users.filter(name__icontains=keyword) #根据关键字对用户姓名信息进行过滤
         print(users)
     return render(request, 'hello/index.html', {'users':users, "keyword": keyword})
```