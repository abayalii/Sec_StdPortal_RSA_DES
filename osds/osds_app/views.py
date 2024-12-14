from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.

def login(request):
    return render(request,"login.html")

def admin(request):
    return render(request,"admin.html")

def student(request):
    return render(request,"student.html")

def staff(request):
    return render(request,"staff.html")