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