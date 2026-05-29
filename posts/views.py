from django.shortcuts import render
from django.http.response import HttpResponse
def hello_world(request):
    return HttpResponse("<h1> HEllo world")
def about(request):
    return render(request, "about.html")

# Create your views here.
