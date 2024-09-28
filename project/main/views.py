from django.shortcuts import render
from .models import test_collection
from django.http import HttpResponse
# Create your views here.


def test(request): 
    data = test_collection.list_collection_names()
    return HttpResponse(data)


def home(request): 
    return render(request, 'main/base.html', {})