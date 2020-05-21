from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from pure_pagination.mixins import PaginationMixin
from cmdb.models import Type, Host
from django.conf import settings
from utils.alisdk import ECSHandler
from utils.Aliyun_key import ALICLOUD


class TypeListView(LoginRequiredMixin, PermissionRequiredMixin, PaginationMixin, ListView):
    """
    标签类型列表
    """
    model = Type
    paginate_by = 5
    permission_required = 'cmdb.view_type'
    keyword = None

    def get_keyword(self):
        self.keyword = self.request.GET.get('keyword')
        return self.keyword

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.get_keyword()
        if keyword:
            queryset = queryset.filter(Q(name__icontains=keyword) | Q(name_cn__icontains=keyword))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['keyword'] = self.keyword
        return context


class TypeAddView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """
    创建标签类型
    """
    model = Type
    fields = ('name', 'name_cn')
    permission_required = 'cmdb.add_type'
    success_message = '添加 %(name)s 类型成功'

    def get_success_url(self):
        if '_addanother' in self.request.POST:
            return reverse('cmdb:type-add')
        return reverse('cmdb:types')


class TypeEditView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    编辑标签
    """
    model = Type
    fields = ('name', 'name_cn')
    permission_required = 'cmdb.change_type'
    success_message = '标签类型 %(name_cn)s 编辑成功！'

    def get_success_url(self):
        if '_addanother' in self.request.POST:
            return reverse('cmdb:type-add')
        elif '_savedit' in self.request.POST:
            return reverse('cmdb:type-edit', kwargs={'pk': self.object.pk})
        else:
            return reverse('cmdb:types')


class TypeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    删除类型
    """
    model = Type
    permission_required = 'cmdb.delete_type'

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, '{} 标签类型删除成功！'.format(self.object.name_cn))
        return response

    def get_success_url(self):
        return reverse_lazy('cmdb:types')


class HostListView(LoginRequiredMixin, PermissionRequiredMixin, PaginationMixin, ListView):
    model = Host
    permission_required = 'cmdb.view_host'
    paginate_by = 4
    key_word = None

    def get_keyword(self):
        self.keyword = self.request.GET.get('keyword')
        return self.keyword

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.get_keyword()
        if keyword:
            queryset = queryset.filter(Q(hostname__icontains=keyword) | Q(os_name__icontains=keyword))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['keyword'] = self.keyword
        return context


class AliyunSDK(LoginRequiredMixin, PermissionRequiredMixin, View):
    model = Host
    permission_required = 'cmdb.change_host'

    def get(self, request):
        ecs = ECSHandler(ALICLOUD['access_key_id'], ALICLOUD['access_key'], ALICLOUD['region'])
        # return data, True, len(instances) >= page_size
        instances = ecs.get_instances()[0]
        for instance in instances:
            is_oldhost = Host.objects.filter(public_ip=instance['public_ip'], private_ip=instance['private_ip'])
            if not is_oldhost:
                Host.objects.create(**instance)
                res = {"code": 0, "msg": "主机列表刷新成功，有新增主机{}".format(instance['hostname'])}
            else:
                Host.objects.update(**instance)
                # object_list = Host.objects.all()
                res = {"code": 0, "msg": "刷新完成，主机数不变~"}
            return render(request, settings.JUMP_PAGE, res)


class StopHostView(View):
    model = Host

    def get(self, request, **kwargs):
        ecs = ECSHandler(ALICLOUD['access_key_id'], ALICLOUD['access_key'], ALICLOUD['region'])
        instance = Host.objects.get(instance_id=kwargs['pk'])
        if instance.status == "Running":
            ecs.stop_host(kwargs['pk'])
            res = {"code": 0, "msg": "操作成功，正在关机~"}
            new_flush = AliyunSDK()
            new_flush.get(request)
        else:
            res = {"code": 1, "errmsg": "服务器繁忙，请稍后重试"}
        return render(request, settings.JUMP_PAGE, res)


class StartHostView(View):
    model = Host

    def get(self, request, **kwargs):
        ecs = ECSHandler(ALICLOUD['access_key_id'], ALICLOUD['access_key'], ALICLOUD['region'])
        instance = Host.objects.get(instance_id=kwargs['pk'])
        if instance.status == "Running":
            res = {"code": 1, "errmsg": "主机正在运行，无需启动~"}
        elif instance.status == "Stopped":
            ecs.start_host(kwargs['pk'])
            res = {"code": 0, "msg": "操作成功，正在启动~"}
            new_flush = AliyunSDK()
            new_flush.get(request)
        else:
            res = {"code": 2, "errmsg": "服务器繁忙，请稍后重试！"}
        return render(request, settings.JUMP_PAGE, res)


class RebootHostView(View):
    model = Host

    def get(self, request, **kwargs):
        ecs = ECSHandler(ALICLOUD['access_key_id'], ALICLOUD['access_key'], ALICLOUD['region'])
        instance = Host.objects.get(instance_id=kwargs['pk'])
        if instance.status == "Running":
            ecs.reboot_host(kwargs['pk'])
            res = {"code": 0, "msg": "操作成功，正在重新启动~"}
            new_flush = AliyunSDK()
            new_flush.get(request)
        elif instance.status == "Stopped":
            ecs.start_host(kwargs['pk'])
            res = {"code": 0, "msg": "操作成功~"}
            new_flush = AliyunSDK()
            new_flush.get(request)
        else:
            res = {"code": 1, "msg": "服务器繁忙，请稍后再试~"}
        return render(request, settings.JUMP_PAGE, res)