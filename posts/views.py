from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from .models import Category, Post
from .forms import PostForm, CategoryForm, UserForm, LoginForm

class AboutView(TemplateView):
    template_name = "about.html"

class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/create_post.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class MyPostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/my_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_edit.html'
    success_url = reverse_lazy('my_posts')

    def test_func(self):
        return self.get_object().user == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts/delete_post.html'
    success_url = reverse_lazy('my_posts')

    def test_func(self):
        return self.get_object().user == self.request.user

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/create_category.html'
    success_url = reverse_lazy('post_create')

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'categories/category_delete.html'
    success_url = reverse_lazy('categories-list')

class RegisterView(FormView):
    form_class = UserForm
    template_name = "register/registration.html"
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        email = form.cleaned_data.get("email", "")
        password = form.cleaned_data["password"]
        user = User.objects.create_user(username=username, email=email, password=password)
        login(self.request, user)
        return super().form_valid(form)

class LoginUserView(LoginView):
    form_class = LoginForm
    template_name = "register/login.html"
    next_page = 'post_list'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop('request', None)
        return kwargs

    def form_invalid(self, form):
        form.add_error(None, "Неверный логин или пароль")
        return super().form_invalid(form)

class LogoutUserView(LogoutView):
    next_page = 'post_list'