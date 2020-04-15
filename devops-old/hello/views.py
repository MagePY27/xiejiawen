from django.shortcuts import render, get_object_or_404
from django.http import  HttpResponse, QueryDict, Http404 #注意要导入相应的包Http404
from hello.models import User
import traceback

# def index(request):
#     # 1.普通传参
#     year = request.GET['year']
#     month = request.GET['month']
#     # year = request.GET.get('year', '2020') #设置默认值的方式更加优雅，注意传参时的encoding
#     # month = request.GET.get('month', '03')
#
#     # 2.位置传参，不推荐
#     # http://ip:port/hello/year/month/
#     return HttpResponse("year is %s, month is %s" % (year, month))

      # 3.kwargs关键字传参，推荐
      # http://ip:port/hello/year/month/
# def index(request, **kwargs):
#      print(kwargs)
#      year = kwargs.get('year')
#      month = kwargs.get('month')
#      return HttpResponse("year is %s, month is %s" % (year, month))

# def index(request):
#     print(request.scheme)
#     print(request.method)
#     print(request.headers)
#
#     data = request.GET
#     year = data.get('year', '2020')
#     month = data.get('month', '03')
#     if request.method == 'POST':
#         print(request.scheme)
#         print(request.body)
#         print(QueryDict(request.body).dict())
#         print(request.POST) #获取相应信息中post发送的数据
#         data = request.POST
#         year = data.get('year', year)
#         month = data.get('month', month)
#     return HttpResponse("year is %s, month is %s" % (year, month))

# 模板的使用

from django.shortcuts import render
# template渲染数据到html
def index(request):
     classname = "DevOps"
     books = ['Python','Java','Django']
     user = {'name':'kk','age':18}
     userlist = [ {'name':'kk','age':18}, {'name':'rock','age':19}, {'name':'mage','age':20}]
     return render(request, 'hello/hello.html', \
                    {'classname': classname,"books":books, "user":user, "userlist":userlist })

def list(request):
     users=[
          {'username':'tom', 'user_cname':'tommy', 'age':15},
          {'username':'jerry', 'user_cname':'jerryer', 'age':16},
          {'username':'jone', 'user_cname':'joner', 'age':17}
     ]
     return render(request, 'userlist.html', {'users':users})

def userlist(request):
     """
     1.用户列表
     2.姓名搜索功能
     # http://url/?keyword=aaa
     """
     keyword = request.GET.get("keyword", "")
     print(keyword)
     users = User.objects.all()
     if keyword:
          users = users.filter(name__icontains=keyword)
          print(users)
     return render(request, 'hello/index.html', {'users':users, "keyword": keyword})

def useradd(request):
     """
     添加用户：request获取表单提交的方式有多种
          1.request.POST.get()适用于获取单个变量进行处理的场景
          2.request.POST.dict()适用于将表单所有的数据整体进行处理
          3.Form(request.POST)适用于表单类验证的场景（生产中最常用）
     """
     msg={}
     if request.method == "POST":
          try:
               print(request.POST)
               #方法一
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
               # 方法二
               data = request.POST.dict()
               User.objects.create(**data)
               msg = {'code': 0, "result": "用户添加成功"}
          except Exception as e:
               print(e)
               msg = {'code': 1, "errmsg": "添加用户失败: %s" % traceback.format_exc()}
          finally:
               return render(request, 'hello/index.html', {"msg": msg, "users":User.objects.all()})
     return render(request, 'hello/useradd.html', {"msg": msg})

def userdel(request, user_id):
     try:
          u = User.objects.get(id=user_id) #每次进入删除页面时判断用户是否存在
     except User.DoesNotExist:
          raise Http404("User does not exist")
     msg = {}
     try:
          if u:
               if request.POST.get('delete') == 'True':
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

def usermod(request, user_id):
     try: #用户存在性检查
          m = User.objects.get(id=user_id)
          # user = get_object_or_404(id=user_id) #更简便地判断用户是否存在，不存在返回404
     except User.DoesNotExist:
          raise Http404("User does not Exist!")
     if request.method == 'POST': #接受前端数据
          try:
               data = request.POST.dict()
               User.objects.filter(id=user_id).update(**data) #解析数据然后更新
               msg={'code': 0, 'result': '用户更新成功'}
               return render(request, 'hello/index.html', {'users': User.objects.all(), 'msg': msg})  # 修改完成则自动返回用户页面
          except Exception as e:
               msg={'code': 1, 'result': '用户更新失败 %s' % traceback.format_exc()}
               return render(request, 'hello/index.html', {'users': User.objects.all(), 'msg': msg})
     return render(request, 'hello/usermod.html', {'user': m}) #跳转至修改页面进行修改

def user():
     pass