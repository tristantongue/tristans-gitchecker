from django.db import models

class Repo(models.Model):
    name = models.CharField(max_length=127)
    size = models.CharField(max_length=127)
    language = models.CharField(max_length=127)

# Create your models here.
