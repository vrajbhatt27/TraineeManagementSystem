from django.db import models
from django.contrib.auth.models import User


class Form(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    fid = models.CharField(max_length=50, null=True)
    date = models.CharField(max_length=15, null=True)
    description = models.CharField(max_length=100, null=True)
    domains = models.CharField(max_length=200, null=True)
    form_status = models.BooleanField()

    def __str__(self):
        return self.fid


class Trainee(models.Model):
    fid = models.CharField(max_length=50, null=True)
    trainee_name = models.CharField(max_length=50, null=True)
    trainee_email = models.CharField(max_length=50, null=True)
    trainee_age = models.IntegerField(null=True)
    trainee_college = models.CharField(max_length=50, null=True)
    trainee_cgpa = models.FloatField(null=True)
    trainee_hsc = models.FloatField(null=True)
    trainee_ssc = models.FloatField(null=True)
    trainee_domain = models.CharField(max_length=50, null=True)
    trainee_resume = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.trainee_email


class Test(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    test_id = models.CharField(max_length=50, null=True)
    domain = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=100, null=True)
    questions = models.JSONField(null=True)
    test_status = models.BooleanField()
