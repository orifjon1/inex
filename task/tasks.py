from django.db.models import Q
from datetime import datetime
from config.celery import app
from task.models import Task


@app.task()
def update_task_missed():
    tasks = Task.objects.filter(Q(deadline__lt=datetime.now().date()) & Q(status='doing'))
    if tasks:
        for task in tasks:
            task.status = 'missed'
            task.save()
    tasks = Task.objects.filter(Q(deadline__gt=datetime.now().date()) & Q(status='missed'))
    if tasks:
        for t in tasks:
            t.status = 'doing'
            t.save()
