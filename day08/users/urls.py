from django.urls import path, re_path
from users import views, views2
from django.conf import settings


app_name = 'users'
urlpatterns = [
    # 单词别写错了，不然会报循环引用
    # path('', views.test, name='test'),
    path('userlistjsview/', views2.UserListJsView.as_view(), name='userlistJsview'),
    path('user_permlist/', views2.UserPermListView.as_view(), name='user_permlist'),
    path('useraddjsview/', views2.UserAddJsView.as_view(), name='useraddJsview'),
    re_path('userdeljsview/(?P<pk>[0-9]{1,})?', views2.UserDelJsView.as_view(), name='userdelJsview'),
    re_path('usermod/(?P<pk>[0-9]{1,})?', views2.UserModJsView.as_view(), name='usermodJsview'),
    re_path('userinfojsview/(?P<pk>[0-9]{1,})?', views2.UserInfoJsView.as_view(), name='userinfoJsview'),
    # re_path('index/(?P<pk>[0-9]{1,})?', views2.IndexJsView.as_view(), name='index'),
    path('index/', views2.IndexView.as_view(), name='index'),

    path('group_list/', views2.GroupListView.as_view(), name='group_list'),
    path('group_add/', views2.GroupAddView.as_view(), name='group_add'),
    re_path('group_add_user/(?P<pk>[0-9]{1,})?', views2.GroupAddUserView.as_view(), name='group_add_user'),
    re_path('group_update/(?P<pk>[0-9]{1,})?', views2.GroupUpdateView.as_view(), name='group_update'),
    re_path('group_delete/(?P<pk>[0-9]{1,})?', views2.GroupDeleteView.as_view(), name='group_delete'),

    # path('111', views2.UserActiveView.as_view(), name='user_active'),
    path('icon', views2.test.as_view(), name='icon'),

    re_path('useractive/(?P<pk>[0-9]{1,})?', views2.UserActiveView.as_view(), name='user_active'),

    re_path('user_group/(?P<pk>[0-9]+)?/', views2.UserGroupView.as_view(), name='user_group_update'),
    re_path('user_perm/(?P<pk>[0-9]+)?/', views2.UserPermissionUpdateView.as_view(), name='user_perm_update'),
    re_path('reset_password/(?P<pk>[0-9]+)?/', views2.ResetPasswordView.as_view(), name='reset_password'),

]
# handler404 = views2.page_not_found