from django.urls import path
from . import views 

urlpatterns = [
    path('test', views.test),
    path('', views.home), 
    path('upload', views.syllabus_upload, name='upload_pdf'), 
]