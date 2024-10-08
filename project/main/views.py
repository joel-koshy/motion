from django.shortcuts import render
from .models import Files, Events, Course, Notes
from django.http import HttpResponse, JsonResponse
from .gemini_sandbox import get_ai_output
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.core import serializers
import json 
# Create your views here.

def syllabus_upload(request): 
    if request.method == 'POST' : 
        file = Files.objects.create(file=request.FILES.get('pdf'))
        res = get_ai_output(file.file.path)
        Course.objects.create(
            student = request.user, 
            title = request.POST['course']
        )

        for event in res: 
            eventType = event['eventType']
            title = event['title']
            start = event['start']
            Events.objects.create(
                eventType = eventType,
                title = title, 
                start = start, 
                user = request.user,
                backgroundColor = request.POST['color'],
                course = request.POST['course']
            )
            print(event)

        queryset = Events.objects.filter(user = request.user)
        serialized_queryset = serializers.serialize('json', queryset)
        context = {
            "calendarEvents":serialized_queryset
        }
        return render(request, 'main/upload_pdf.html', context)
        
        json_parsed = json.dumps(res)

        context = {
            "calendarEvents": json_parsed
        }
        print(type(res))
        print(res)

        
        # return JsonResponse(res, safe=False)
        return render(request, 'main/upload_pdf.html', context) 
    
    elif request.method == 'GET':
        queryset = Events.objects.filter(user = request.user)
        serialized_queryset = serializers.serialize('json', queryset)
        context = {
            "calendarEvents":serialized_queryset
        }
        return render(request, 'main/upload_pdf.html', context)
    
def tracker_page(request):
    if request.method == 'GET':
        queryset = Events.objects.filter(user = request.user).order_by('start')
        serialized_queryset = serializers.serialize('json', queryset)
        context = {
            "calendarEvents": queryset.values()
        }
        return render(request, 'main/Assignment_Tracker.html', context)
    elif request.method == 'POST': 
        Events.objects.create(
            eventType=request.POST['type'],
            start=request.POST['date'], 
            course=request.POST['course'], 
            title=request.POST['title'],
            user=request.user  
        )
        queryset = Events.objects.filter(user = request.user).order_by('start')
        serialized_queryset = serializers.serialize('json', queryset)
        context = {
            "calendarEvents": queryset.values()
        }
        return render(request, 'main/Assignment_Tracker.html', context) 

def tracker_page_sort(request, order): 
    if request.method == 'GET': 
        queryset = Events.objects.filter(user = request.user).order_by(order)
        serialized_queryset = serializers.serialize('json', queryset)
        context = {
            "calendarEvents": queryset.values()
        }

        return render(request, 'main/Assignment_Tracker.html', context)

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

def notes(request):
    if request.method == 'GET': 
        querySet = Course.objects.filter(student = request.user)
        note_querySet = Notes.objects.filter(author = request.user)

        context = {
            "Courses":querySet.values, 
            "Notes":note_querySet.values(), 
        }
        return render(request, 'main/Notes_Tracker.html',context)
    
    elif request.method == 'POST': 
        course = Course.objects.filter(title = request.POST['Course']).first()

        Notes.objects.create(
            author=request.user, 
            course = course,
            note = request.FILES.get('note') 
        )

        querySet = Course.objects.filter(student = request.user)
        note_querySet = Notes.objects.filter(author = request.user)

        context = {
            "Courses":querySet.values(), 
            "Notes":note_querySet.values(), 
        }
        return render(request, 'main/Notes_Tracker.html',context)
 