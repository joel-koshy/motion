from django.db import models
from .db_connection import client
# Create your models here.

test_collection = client['sample_mflix']

class Files(models.Model): 
    file = models.FileField(upload_to="syllabus")