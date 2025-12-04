from django.shortcuts import render

def home(request):
    return render(request, "index.html")
def services(request):
    return render(request,"services.html")
def about(request):
    return render(request,"about.html")
def work(request):
    return render(request,"process.html")
def contact(request):
    return render(request,"contact.html")
def login(request):
    return render(request,"login.html")