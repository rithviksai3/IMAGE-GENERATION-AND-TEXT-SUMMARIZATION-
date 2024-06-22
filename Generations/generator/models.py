from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Detail(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    prompt = models.TextField()
    date= models.DateTimeField()

class Idetail(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    prompt = models.TextField()
    date = models.DateTimeField()

class Contact(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    cname=models.CharField(max_length=10)
    subject=models.TextField()