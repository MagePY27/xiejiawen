from django.urls import path, re_path
from hello import views, views2

app_name = 'hello'
urlpatterns = [
    path('', views.index, name='index'),
    path('userlistformview/', views2.UserListFormView.as_view(), name='userlistFormview'),
    path('useraddformview/', views2.UserAddFormView.as_view(), name='useraddFormview'),
    re_path('userdetailformview/(?P<pk>[0-9]{1,})?', views2.UserDetailFormView.as_view(), name='userdetailFormview'),
    re_path('userdelformview/(?P<pk>[0-9]{1,})?', views2.UserDelFormView.as_view(), name='userdelFormview'),

]