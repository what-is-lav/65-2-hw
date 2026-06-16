from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from .models import Category, Post
from .forms import PostForm, CategoryForm, UserForm, LoginForm

def hello_world(request):
    return HttpResponse("<h1>HellO world</h1>")

def about(request):
    return render(request, "about.html")

def active_categories_list(request):
    categories = Category.objects.filter(is_active=True)
    context = {'categories': categories}
    return render(request, 'categories/categories_list.html', context)

def list_view(request):
    posts = Post.objects.all()
    categories = Category.objects.filter(is_active=True) 
    context = {'posts': posts, 'categories': categories}
    return render(request, 'posts/post_list.html', context)

def detail_view(request, pk):
    post = Post.objects.filter(pk=pk).first()
    context = {'post': post}
    return render(request, 'posts/post_detail.html', context)

def post_create(request):
    if not request.user.is_authenticated:
        return redirect('post_list')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'posts/create_post.html', context)

def my_posts(request):
    if not request.user.is_authenticated:
        return redirect('post_list')

    posts = Post.objects.filter(user=request.user)
    context = {'posts': posts}
    return render(request, 'posts/my_posts.html', context)

def post_edit(request, pk):
    if not request.user.is_authenticated:
        return redirect('post_list')

    post = Post.objects.filter(pk=pk).first()
    
    if not post or post.user != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('my_posts')
    else:
        form = PostForm(instance=post)
        
    context = {'form': form, 'post': post}
    return render(request, 'posts/post_edit.html', context)

def post_delete(request, pk):
    if not request.user.is_authenticated:
        return redirect('post_list')
    
    post = get_object_or_404(Post, pk=pk, user=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('my_posts')
    return render(request, 'posts/delete_post.html', {'post': post})

def category_create(request):
    if not request.user.is_authenticated:
        return redirect('post_list')
        
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_create')
    else:
        form = CategoryForm()
        
    return render(request, 'categories/create_category.html', {'form': form})

def category_delete(request, pk):
    if not request.user.is_authenticated:
        return redirect('categories-list')
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('categories-list')
    return render(request, 'categories/category_delete.html', {'category': category})

def register_user(request):
    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        try:
            if form.is_valid():
                email = form.cleaned_data["email"]
                user = User(username=email, email=email)
                raw_password = form.cleaned_data["password"]
                user.set_password(raw_password)
                user.save()
                login(request, user)
                return redirect("post_list")
        except IntegrityError:
            form.add_error("email", "Пользователь с таким email уже существует!")
            
    return render(request, "register/registration.html", context={"form": form})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('post_list')
            else:
                form.add_error(None, "Неверный логин или пароль")
    else:
        form = LoginForm()
    
    return render(request, "register/login.html", context={"form": form})

def logout_user(request):
    logout(request)
    return redirect('post_list')
