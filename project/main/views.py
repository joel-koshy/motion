from django.shortcuts import render
from .models import test_collection, Files
from django.http import HttpResponse, JsonResponse
from .gemini_sandbox import get_ai_output

# Create your views here.


def test(request): 
    data = test_collection.list_collection_names()
    return HttpResponse(data)

def syllabus_upload(request): 
    if request.method == 'POST' : 
        data = {
            "pdf":request.FILES.get('pdf')
        }
    
        # res = get_ai_output(request.FILES.get('pdf'))
        file = Files.objects.create(file=request.FILES.get('pdf'))
        res = get_ai_output(file.file.path)
        # print(type(res))
        return JsonResponse(res)
    
    elif request.method == 'GET':
        return render(request, 'main/upload_pdf.html', {})
    



def home(request): 
    return render(request, 'main/base.html', {})