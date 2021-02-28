from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Teacher)
admin.site.register(Exercise)
admin.site.register(Student)
admin.site.register(Submission)
admin.site.register(Solution)
