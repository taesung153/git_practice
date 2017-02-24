from django.shortcuts import render, redirect
from .models import Course


# Create your views here.

def index(request):
    context={
    "Courses" : Course.objects.all()
    }
    print Course.objects.all()
    return render(request, 'course/index.html', context)

def Courses(request):
    print request.POST
    Course.objects.create(course_name=request.POST['Course_Name'], description=request.POST['Description'])
    return redirect('/')

def remove(reqeust, id):
    Course.objects.filter(id = id).delete()
    return redirect('/')

def confirm(reqeust, id):
    context = {
        "deletes" : Course.objects.filter(id = id)
    }
    return render(reqeust, 'course/del.html', context)

def back(request):
    return render(request, 'course/index.html', context)
