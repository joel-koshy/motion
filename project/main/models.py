from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Files(models.Model): 
    file = models.FileField(upload_to="syllabus")

class Course(models.Model): 
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)

class Events(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    eventType = models.CharField(max_length=15)
    title = models.CharField(max_length=100)
    start = models.CharField(max_length=20)
    end=models.CharField(max_length=20, blank=True, null=True)
    backgroundColor = models.CharField(max_length=20, null=True)
    course = models.CharField(max_length=20, null=True)
   
    def __str__(self) -> str:
        return (" " + self.title)
    

class Notes(models.Model): 
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    note = models.FileField(upload_to="notes")

    
