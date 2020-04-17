from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("<p>this is a test page</p>")
# Create your views here.
