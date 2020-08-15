from django.db import models
from django.contrib.auth.models import User
#for some weird reason vscode shows error for above eventhoght issa correct
#so to avoid that you could write from django.contrib.auth import User and..
#for the bottom code implementation you have to write models.User instead of just writing User
from datetime import date

# Create your models here.


class review(models.Model):
    company = models.CharField(max_length=50)
    currentStat = models.CharField(max_length=20)
    jobtitle = models.CharField(max_length=50)
    reviewHeadline = models.CharField(max_length=50)
    pros = models.TextField()
    cons = models.TextField()
    person = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.company+" review"
    
class blog(models.Model):
    title = models.CharField(max_length=50)
    img= models.ImageField(default=None,null = True, blank=True)
    body = models.TextField()
    day = models.DateField(auto_now_add=True, blank=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
