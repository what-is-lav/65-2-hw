from django.db import models

class Post(models.Model):
    title = models.CharField()
    content = models.TextField()
    rate = models.IntegerField()

# Create your models here.
