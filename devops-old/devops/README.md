# P27N11-xiejiawen
learn python, team of magedu.com

```
date: 2020/03/27
author: xiejiawen
env: pycharm(django-2.2 + mysqlclient-1.4.6) + linux(mariadb-5.5.6)
```

1.先在pycharm的terminal中创建一个django项目，取名为devops
django-admin startproject devops

2.进入devops/devops目录，修改setting.py文件

`ALLOWED_HOSTS = ['*']`



```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'devops',
        'HOST': '192.168.99.105', #数据库ip
        'USER': 'python',
        'PASSWORD': 'aaa',
        'PORT': '3306',
        'OPTIONS': {            #如果数据库设置为strict模式时，需要此选项
            'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"',
            'charset': 'utf8mb4'
        }
    }
}
```

```bash
LANGUAGE_CODE = 'en-us' #修改语言

TIME_ZONE = 'Asia/Shanghai' #如果设置此语句，则需设置`USE_TZ = False`

USE_I18N = True

USE_L10N = True

USE_TZ = False
```
`
(1)创建数据库
~]$ mysql -upython -p
> create database devops;
(2)导入devops数据
> python manage.py migrate
(3)启动服务
~]$ python manage.py runserver 0.0.0.0:8081
(4)访问默认页面
curl -I http://192.168.99.1:8081/admin/
`

3.先在pycharm的terminal中创建一个服务模块hello

`python manage.py startapp hello`

4.创建文件devops/hello/urls.py
```python
from django.urls import path
from . import views #使用主路由+路由时需要导入文件

urlpatterns = [
    path('hello/', views.index, name='hello'),
]
```

5.修改hello的数据文件devops/hello/views.py
```python
from django.shortcuts import render
from django.http import  HttpResponse
# Create your views here.

def index(request): #请求到来时，返回下面这句
    return HttpResponse("<p>hello world !</p>")
```

6.修改devops/devops/urls.py文件，给hello服务添加路由
```python
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from hello import views #只使用主路由时，需要导入服务文件

urlpatterns = [
    #path('hello/', views.index),   #使用主路由访问，
                                    #此语句生效时，devops/hello/urls.py文件中的内容要注释掉
    path('admin/', admin.site.urls),
    path('hello/', include('hello.urls')) #使用主路由+子路由
]
```

6.在terminal中启动服务(需要在devops/目录下运行命令)
```bash
python manage.py runserver 0.0.0.0:8081
```

7.局域网内访问
```bash
curl -I http://192.168.99.1:8081/hello #主路由
#返回HTTP/1.1 200 OK
curl -I http://192.168.99.1:8081/hello/hello/ #主路由+自路由
#返回HTTP/1.1 200 OK
```