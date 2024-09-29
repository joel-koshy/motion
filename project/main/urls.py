from django.urls import path
from . import views 

urlpatterns = [
    path('test', views.test),
    path('', views.home), 
    path('upload', views.syllabus_upload, name='upload_pdf'), 
    path('login', views.alogin, name='login_page'), 
    path('signup', views.create_new_user, name='signup_page'),
    path('logout', views.alogout, name='logout'),
    path('tracker', views.tracker_page, name='tracker_page'), 
    path('notes', views.notes, name='notes_page'), 

]