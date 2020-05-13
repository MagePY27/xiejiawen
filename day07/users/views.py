from django.shortcuts import render
from django.http import HttpResponse

def test(request):
    return HttpResponse("this is a test page")

# Create your views here.
