from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
   
   
class Post(models.Model):
    title = models.CharField()
    content = models.TextField()
    rate = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='posts')


# Create your models here.
