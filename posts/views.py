from django.shortcuts import render
from django.http.response import HttpResponse
from .models import Category,Post
from django.views.generic import ListView, DetailView

def hello_world(request):
    return HttpResponse("<h1>HellO world</h1>")

def about(request):
    return render(request, "about.html")

def active_categories_list(request):
    categories = Category.objects.filter(is_active=True)
    context = {'categories': categories}
    return render(request, 'categories_list.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'