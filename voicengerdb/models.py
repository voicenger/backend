from django.db import models

class User(models.Model):
    name = models.CharField(max_length=140)
    nickname = models.CharField(max_length=50)
    age = models.IntegerField()