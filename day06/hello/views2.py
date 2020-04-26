from django.shortcuts import render, reverse
from django.http import JsonResponse, QueryDict
from django.views.generic import ListView, TemplateView, DetailView
from django.db.models import Q, F
from hello.models import Project_User
from django.conf import settings

class UserListJsView(ListView):
    template_name = 'hello/userlist.html'
    model = Project_User
    context_object_name = "users"

    def get_queryset(self):
        queryset = super(UserListJsView, self).get_queryset()
        self.keyword = self.request.GET.get("keyword", "").strip()
        if self.keyword:
            queryset = queryset.filter(Q(name__icontains=self.keyword) | Q(phone__icontains=self.keyword))
        return queryset


class UserAddJsView(TemplateView):
    pass

class UserDelJsView(DetailView):
    pass

class UserModJsView(DetailView):
    pass