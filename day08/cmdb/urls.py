from django.urls import path, re_path
from cmdb.views import *
from cmdb.tag import *


app_name='cmdb'
urlpatterns = [
    # path('', test, name='test'),
    path('index/', IndexView.as_view(), name='index'),

    path('types/', TypeListView.as_view(), name='types'),
    path('types_add/', TypeAddView.as_view(), name='type-add'),
    re_path('types_edit/(?P<pk>[0-9]+)?/', TypeEditView.as_view(), name='type-edit'),
    re_path('types_delete/(?P<pk>[0-9]+)?/', TypeDeleteView.as_view(), name='type-delete'),

    path('tags/', TagListView.as_view(), name='tags'),
    path('tags_add/', TagAddView.as_view(), name='tag-add'),
    re_path('tags_edit/(?P<pk>[0-9]+)?/', TagEditView.as_view(), name='tag-edit'),
    re_path('tags_delete/(?P<pk>[0-9]+)?/', TagDeleteView.as_view(), name='tag-delete'),

    path('hosts/', HostListView.as_view(), name='hosts'),
    path('get_host/', AliyunSDK.as_view(), name='get_host'),
    re_path('stop_host/(?P<pk>[0-9a-z-]+)?/', StopHostView.as_view(), name='stop_host'),
    re_path('start_host/(?P<pk>[0-9a-z-]+)?/', StartHostView.as_view(), name='start_host'),
    re_path('reboot_host/(?P<pk>[0-9a-z-]+)?/', RebootHostView.as_view(), name='reboot_host'),

    re_path('hosts_tags_add/(?P<pk>[0-9]+)?/', HostTagAddView.as_view(), name='host-tags-add'),
    re_path('tags_addhosts/(?P<pk>[0-9]+)?/', HostAddByTagView.as_view(), name='add-hosts'),
    path('update_host_info/', update_host_info, name='update-host-info'),
    path('overview/', AssetsOverView.as_view(), name='overview'),
]