from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
   
   
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    rate = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='posts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

# Create your models here.
