from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Files(models.Model): 
    file = models.FileField(upload_to="syllabus")

class Events(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    eventType = models.CharField(max_length=15)
    title = models.CharField(max_length=100)
    start = models.CharField(max_length=20)

    class Meta: 
        unique_together = (('title'), ('start'))
    
    def __str__(self) -> str:
        return (" " + self.title)