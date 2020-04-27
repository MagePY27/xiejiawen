from django.urls import path, re_path
from hello import views, views2
from django.conf import settings


app_name = 'hello'
urlpatterns = [
    # 单词别写错了，不然会报循环引用
    # path('', views.index, name='index'),
    path('userlistjsview/', views2.UserListJsView.as_view(), name='userlistJsview'),
    path('useraddjsview/', views2.UserAddJsView.as_view(), name='useraddJsview'),
    re_path('userdeljsview/(?P<pk>[0-9]{1,})?', views2.UserDelJsView.as_view(), name='userdelJsview'),
    re_path('usermodjsview/(?P<pk>[0-9]{1,})?', views2.UserModJsView.as_view(), name='usermodJsview'),

    path('index/', views2.IndexJsView.as_view(), name='index'),
    path('login/', views2.UserLoginJsView.as_view(), name='login'),
]
handler404 = views2.page_not_found