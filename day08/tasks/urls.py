from django.urls import path, re_path
from .views import *

app_name = 'task'

urlpatterns = [
    path('add/', TaskAddView.as_view(), name='task_add'),
    path('list/', TaskListView.as_view(), name='task_list'),
    re_path('task_detail/(?P<pk>[0-9]+)?/', TaskDetailView.as_view(), name='task_detail'),
    re_path('edit/(?P<pk>[0-9]+)?/', TaskEditView.as_view(), name='task_edit'),
#
    re_path('publish/(?P<pk>[0-9]+)?/', task_publish, name='task_publish'),
#     path('get_task_result/', get_task_result, name='get_task_result'),
#
    path('history/', TaskHistoryListView.as_view(), name='history'),
    path('get_playbook/', get_playbook, name='get_playbook'),
]
