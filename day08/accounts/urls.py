from django.urls import path, re_path
from accounts import views


app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    re_path('pwdmod/(?P<pk>[0-9]{1,})?', views.UserPwdView.as_view(), name='pwdmod'),

    path('permlist/', views.PermListView.as_view(), name='permlist'),
    re_path('permupdate/(?P<pk>[0-9]{1,})?', views.PermUpdateView.as_view(), name='permupdate'),
]