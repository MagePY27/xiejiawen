from django.urls import path, re_path
from hello import views, views2


urlpatterns = [
    path('', views.index, name='index'),
    path('formview/', views2.UserFormView.as_view(), name='formview'),
]