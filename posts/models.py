from django.db import models

class Post(models.Model):
    title = models.CharField()
    content = models.TextField()
    rate = models.IntegerField()

class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

# Create your models here.
