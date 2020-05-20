from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from pure_pagination.mixins import PaginationMixin

from cmdb.models import Tag, Type, Host


class TagListView(LoginRequiredMixin, PermissionRequiredMixin, PaginationMixin, ListView):
    """
    标签列表
    """
    model = Tag
    paginate_by = 6
    permission_required = 'cmdb.view_tag'
    keyword = None

    def get_keyword(self):
        self.keyword = self.request.GET.get('keyword')
        return self.keyword

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.get_keyword()
        if keyword:
            queryset = queryset.filter(Q(name__icontains=keyword) | Q(name_cn__icontains=keyword) |
                                       Q(type__name__icontains=keyword) | Q(type__name_cn__icontains=keyword))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['keyword'] = self.keyword
        return context


class TagAddView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """
    创建标签
    """
    model = Tag
    fields = ('type', 'name', 'name_cn')
    permission_required = 'cmdb.add_tag'
    success_message = '添加 %(name_cn)s 标签成功~'

    def get_success_url(self):
        if '_addanother' in self.request.POST:
            return reverse('cmdb:tag-add')
        return reverse('cmdb:tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = Type.objects.all()
        return context


class TagEditView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    编辑标签
    """
    model = Tag
    fields = ('type', 'name', 'name_cn')
    permission_required = 'cmdb.change_tag'
    success_message = '%(name_cn)s 标签编辑成功！'

    def get_success_url(self):
        if '_addanother' in self.request.POST:
            return reverse('cmdb:tag-add')
        elif '_savedit' in self.request.POST:
            return reverse('cmdb:tag-edit', kwargs={'pk': self.object.pk})
        return reverse('cmdb:tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = Type.objects.all()
        return context


class TagDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    删除标签
    """
    model = Tag
    permission_required = 'cmdb.delete_tag'

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, '{} 标签删除成功！'.format(self.object.name_cn))
        return response

    def get_success_url(self):
        return reverse_lazy('cmdb:tags')