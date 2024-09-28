from django.shortcuts import render
from .models import test_collection
from django.http import HttpResponse
# Create your views here.


def test(request): 
    data = test_collection.list_collection_names()
    return HttpResponse(data)

def syllabus_upload(request): 
    if request.method == 'POST' : 
        data = {
            "pdf":request.FILES.get('pdf')
        }
        print("Hello")
        print(data)
        return HttpResponse()
    
    elif request.method == 'GET':
        return render(request, 'main/upload_pdf.html', {})
    



def home(request): 
    return render(request, 'main/base.html', {})