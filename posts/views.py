from django.shortcuts import render
from django.http.response import HttpResponse
from .models import Category

def hello_world(request):
    return HttpResponse("<h1>HellO world</h1>")

def about(request):
    return render(request, "about.html")

def active_categories_list(request):
    categories = Category.objects.filter(is_active=True)
    context = {'categories': categories}
    return render(request, 'categories_list.html', context)