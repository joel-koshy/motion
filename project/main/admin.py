from django.contrib import admin
from .models import Files, Events, Course, Notes
# Register your models here.
admin.site.register(Files)
admin.site.register(Events)
admin.site.register(Course)
admin.site.register(Notes)


