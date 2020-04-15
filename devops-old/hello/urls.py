#!/usr/bin/python
# coding=utf-8
# 使用主路由+子路由时，下列语句需要启用
# from django.urls import path,re_path
# from . import views
#
# urlpatterns = [
#     path('hello/', views.index, name='hello'),
#     # 1.path('', views.index, name='index'),
#     # 2.re_path('([0-9]{4})/([0-9]{2})/', views.index, name='index'),  #需要import re_path
#     # 3.re_path('(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/', views.index,
#     # name='index')
#     # re_path('(?P<year>[0-9]{4})/(?P<month>[0-9]{1,})/', views.index, name='index')
# ]

from django.urls import path, re_path
from . import views, views2
app_name = 'hello'
urlpatterns = [
    path('', views.index, name='index'),
    # path('list/', views.list, name='list'),
    path('userlist/', views.userlist, name = 'userlist'),
    path('useradd/', views.useradd, name = 'useradd'),
    re_path('userdel/(?P<user_id>[0-9]{1,})', views.userdel, name='userdel'), #name命名空间
    re_path('usermod/(?P<user_id>[0-9]{1,})', views.usermod, name='usermodefy'),

    # FBV实现增删改查
    # path('index/', views2.index, name='index'),

    # 通用视图
    # as_view源码中的dispatch函数将用户请求，method映射成对应的function
    # path('index/', views2.IndexView.as_view()),

    # View
    path('index1/', views2.IndexView1.as_view(), name='index1'),

    # TemplateView
    path('index2/', views2.IndexView2.as_view(), name='index2'),
    # re_path('index2/(?P<pk>[0-9]+)?/', views2.IndexView2.as_view(), name='index2'),

    #ListView -- 查询数据表的所有数据，很常用
    path('index3/', views2.IndexView3.as_view(), name='index3'),

    #DetailView -- 查询数据表的某一条数据
    re_path('index4/(?P<pk>[0-9]+)?/', views2.IndexView4.as_view(), name='index4'),

    # CreateView -- 创建数据
    path('index5/', views2.IndexView5.as_view(), name='index5'),

    #UpdateView -- 更新数据
    re_path('index6/(?P<pk>[0-9]+)?/', views2.IndexView6.as_view(), name='index6'),

    #DeleteView -- 删除数据
    re_path('index7/(?P<pk>[0-9]+)?/', views2.IndexView7.as_view(), name='index7'),
    # path('index7/', views2.IndexView7.as_view(), name='index7'),
]