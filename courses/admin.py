from django.contrib import admin
from .models import Course, Facility, Instructor, Biography, JobTitle, SyllabusData

# Models are registered here
admin.site.register(Course)
admin.site.register(Facility)
admin.site.register(Instructor)
admin.site.register(Biography)
admin.site.register(JobTitle)
admin.site.register(SyllabusData)