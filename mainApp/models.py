from django.db import models
from django.contrib.auth.models import User

class Form(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    fid = models.CharField(max_length=50, null=True)
    date = models.CharField(max_length=15, null=True)
    description = models.CharField(max_length=100, null=True)
    domains = models.CharField(max_length=200, null=True)
    form_status = models.BooleanField()