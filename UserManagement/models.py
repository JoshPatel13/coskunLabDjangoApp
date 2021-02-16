from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=100, unique=True)
    role = models.CharField(max_length=15)
    phone_number = models.IntegerField(blank=True, null=True, unique=True)
    is_deleted = models.BooleanField(default = False)


class Research(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=4000)
    due_date = models.DateTimeField()
    approved = models.BooleanField()

class Dashboard(models.Model):
    research = models.ForeignKey(Research, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
