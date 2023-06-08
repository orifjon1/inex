from django.contrib import admin
from .models import Task, TaskReview, TaskUpdateTimes


admin.site.register(Task)
admin.site.register(TaskUpdateTimes)
admin.site.register(TaskReview)
