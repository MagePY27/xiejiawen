from django.urls import path, re_path
from cmdb.views import *
from cmdb.tag import *


app_name='cmdb'
urlpatterns = [
    # path('', views.test, name='test'),

    path('types/', TypeListView.as_view(), name='types'),
    path('types_add/', TypeAddView.as_view(), name='type-add'),
    re_path('types_edit/(?P<pk>[0-9]+)?/', TypeEditView.as_view(), name='type-edit'),
    re_path('types_delete/(?P<pk>[0-9]+)?/', TypeDeleteView.as_view(), name='type-delete'),

    path('tags/', TagListView.as_view(), name='tags'),
    path('tags_add/', TagAddView.as_view(), name='tag-add'),
    re_path('tags_edit/(?P<pk>[0-9]+)?/', TagEditView.as_view(), name='tag-edit'),
    re_path('tags_delete/(?P<pk>[0-9]+)?/', TagDeleteView.as_view(), name='tag-delete'),
]