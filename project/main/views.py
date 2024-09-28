from django.shortcuts import render
from .models import test_collection, Files
from django.http import HttpResponse, JsonResponse
from .gemini_sandbox import get_ai_output
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

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


def alogin(request):
    if request.method == 'POST': 

        username=request.POST["username"]
        password=request.POST["password"]
        print(username, password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None: 
            login(request, user)
            print("login worked")
            return redirect("upload_pdf")
        else: 
            return redirect("login_page")
    elif request.method == 'GET': 
        return render(request, 'main/login.html', {})
    
def alogout(request): 
    logout(request)
    return redirect("login_page")

def create_new_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST['password']
        new_user = User.objects.create(username = username)
        new_user.set_password(password)
        new_user.save()
        return redirect('login_page')
    elif request.method == 'GET': 
        return render(request, 'main/signup.html', {})

   