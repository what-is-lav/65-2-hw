from django import forms
from .models import Post, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["title", "description", "is_active"]
        

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "rate", "category"]

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if content and len(content) < 50:
            raise forms.ValidationError("Минимальное количество символов: 50")
        return content
    

class UserForm(forms.Form):
    username = forms.CharField(label="Логин", max_length=150)
    email = forms.EmailField(label="Email (необязательно)", required=False)
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

class LoginForm(forms.Form):
    username = forms.CharField(label="Логин")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")