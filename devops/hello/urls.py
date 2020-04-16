from django.urls import path, re_path
from hello import views, views2

app_name = 'hello'
urlpatterns = [
    path('', views.index, name='index'),
    path('userlist/', views2.UserListView.as_view(), name='userlist'),
    path('useradd/', views2.UserAddView.as_view(), name='useradd'),
    re_path('userdel/(?P<pk>[0-9]{1,})?/', views2.UserDelView.as_view(), name='userdel'),
    re_path('usermod/(?P<pk>[0-9]{1,})?/', views2.UserModView.as_view(), name='usermod'),
]