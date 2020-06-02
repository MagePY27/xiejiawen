import json
import os
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.utils import timezone
from django.core import serializers
from django.views.decorators.http import require_POST, require_GET
from pure_pagination.mixins import PaginationMixin

# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from day08.settings import BASE_DIR
from cmdb.models import Host
from cmdb.models import Tag
from django.contrib.auth import get_user_model
from tasks.models import Task, HistoricTask

User = get_user_model()


class TaskAddView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    添加通用任务
    """
    permission_required = 'tasks.add_task'

    def get(self, request):
        hosts = Host.objects.all()
        tags = Tag.objects.all()
        context = {'hosts': hosts, 'tags': tags}
        return render(request, 'tasks/generaltask_add.html', context=context)


@require_POST
@login_required
def get_playbook(request):
    """
    返回playbook
    :param request:
    :return:
    """
    ids = request.POST.get('ids','')
    print(ids)
    content = request.POST.get('content','')
    print(content)
    ids = json.loads(ids)
    # values_list方法加个参数flat=True返回单个值的QuerySet
    hosts = Host.objects.filter(id__in=ids).values_list('private_ip', flat=True)
    print(hosts)
    if content:
        with open(os.path.join(BASE_DIR, 'tmp', 'tmp_playbook.yml'), 'w') as f:
            f.write(content)
        with open(os.path.join(BASE_DIR, 'tmp', 'tmp_playbook.yml'), 'r') as f:
            content = ''
            for line in f:
                if line.startswith('- hosts'):
                    content += '- hosts: {}\n'.format(','.join(hosts))
                else:
                    content += line
    else:
        content = loader.render_to_string('tasks/playbook_demo.yml.templage', {'dest_hosts': ','.join(hosts)})
    return JsonResponse({'code': 0, 'msg': '获取Playbook demo成功!', 'content': content})





class TaskAddView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    添加通用任务
    """
    permission_required = 'tasks.add_task'

    def get(self, request):
        hosts = Host.objects.all()
        tags = Tag.objects.all()
        context = {'hosts': hosts, 'tags': tags}
        return render(request, 'tasks/generaltask_add.html', context=context)

    def post(self, request):
        ids = request.POST.get('ids')
        ids = json.loads(ids)
        content = request.POST.get('content')
        name = request.POST.get('name')

        task = Task()
        task.name = name
        task.save()
        historic_task = HistoricTask()
        historic_task.task = task
        historic_task.content = content
        historic_task.apply_user = request.user
        historic_task.status = 0
        historic_task.save()
        historic_task.dest_hosts.set(ids)
        messages.success(request, '{} 任务创建成功!'.format(task.name))
        # emails = [user.email for user in User.objects.all() if user.has_perm('task.review_task')]
        # email_send.delay(emails, send_type='audit_task', task=task.name)
        return JsonResponse({'code': 0, 'msg': '任务创建成功'})


class TaskListView(LoginRequiredMixin, PermissionRequiredMixin, PaginationMixin, ListView):
    """
    任务列表
    """
    template_name = 'tasks/task_list.html'
    model = HistoricTask
    paginate_by = 10
    permission_required = 'tasks.view_task'
    keyword = None

    def get_keyword(self):
        self.keyword = self.request.GET.get('keyword')
        return self.keyword

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(status__in=[0, 2])
        keyword = self.get_keyword()
        if keyword:
            queryset = queryset.filter(Q(task__name__icontains=keyword) | Q(dest_hosts__instance_name=keyword) |
                                       Q(dest_dir__icontains=keyword) | Q(content__icontains=keyword) |
                                       Q(version__icontains=keyword) | Q(apply_user__username__icontains=keyword) |
                                       Q(apply_user__name__icontains=keyword) | Q(
                reviewer__username__icontains=keyword) |
                                       Q(reviewer__name__icontains=keyword) | Q(review_notes__icontains=keyword) |
                                       Q(publisher__username__icontains=keyword) | Q(
                publisher__name__icontains=keyword) |
                                       Q(result__icontains=keyword)).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['keyword'] = self.keyword
        return context


class TaskDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    任务详情页
    """
    template_name = 'tasks/task_detail.html'
    model = HistoricTask
    permission_required = 'tasks.view_task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prev'] = self.request.GET.get('prev')
        return context

    def post(self, request, pk):
        status = request.POST.get('status')
        review_notes = request.POST.get('review_notes')
        task = HistoricTask.objects.filter(id=pk).get()
        task.status = status
        task.review_notes = review_notes
        task.reviewer = request.user
        task.review_at = timezone.now()
        task.save()
        status = int(status)
        # if status == 1:
        #     # email_send.delay(task.apply_user.email, send_type='audit_task_refuse', task=task.task.name, id=task.id)
        # elif status == 2:
        #     # email_send.delay(task.apply_user.email, send_type='task_publish', task=task.task.name, id=task.id)
        return JsonResponse({'code': 0, 'msg': '审核成功!'})


class TaskHistoryListView(LoginRequiredMixin, PermissionRequiredMixin, PaginationMixin, ListView):
    """
    任务历史列表
    """
    template_name = 'tasks/task_history_list.html'
    model = HistoricTask
    paginate_by = 10
    permission_required = 'tasks.view_history'
    keyword = None

    def get_keyword(self):
        self.keyword = self.request.GET.get('keyword')
        return self.keyword

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(status__in=[-1, 1, 3])
        keyword = self.get_keyword()
        if keyword:
            queryset = queryset.filter(Q(task__name__icontains=keyword) | Q(dest_hosts__instance_name=keyword) |
                                       Q(dest_dir__icontains=keyword) | Q(content__icontains=keyword) |
                                       Q(version__icontains=keyword) | Q(apply_user__username__icontains=keyword) |
                                       Q(apply_user__name__icontains=keyword) | Q(
                reviewer__username__icontains=keyword) |
                                       Q(reviewer__name__icontains=keyword) | Q(review_notes__icontains=keyword) |
                                       Q(publisher__username__icontains=keyword) | Q(
                publisher__name__icontains=keyword) |
                                       Q(result__icontains=keyword)).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['keyword'] = self.keyword
        return context


class TaskEditView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'tasks.change_task'
    model = Task
    template_name = 'tasks/task_edit.html'


    def post(self, **kwargs):
        pass

def task_publish():
    pass