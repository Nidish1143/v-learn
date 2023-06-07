from django.db import models

# Create your models here.
class assignment(models.Model):
    title=models.CharField(max_length=50)
    asid=models.IntegerField()
    upload=models.FileField(upload_to="file",default='')
    sid=models.IntegerField()
    status=models.CharField(max_length=50)
class question(models.Model):
    subid=models.IntegerField()
    sid=models.IntegerField()
    question=models.CharField(max_length=60)
    answer=models.CharField(max_length=60)
    status=models.CharField(max_length=50)

class Studreg(models.Model):
    name=models.CharField(max_length=30)
    gender=models.CharField(max_length=20)
    dob=models.DateField()
    admno=models.IntegerField()
    dept=models.CharField(max_length=30)
    course=models.CharField(max_length=30)
    semester=models.IntegerField()
    email=models.CharField(max_length=50)
    phno=models.BigIntegerField()
    uname=models.CharField(max_length=20)
    pwd=models.CharField(max_length=20)
class commends(models.Model):
    sid=models.IntegerField()
    comm=models.TextField()
    tid=models.IntegerField()
class quizans(models.Model):
    qid=models.IntegerField()
    ans=models.CharField(max_length=20)
    sid=models.IntegerField()
    date=models.DateField(null=True)