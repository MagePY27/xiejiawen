from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404


# Create your views here.
def index(request):
    return HttpResponse("success")