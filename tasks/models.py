from django.db import models

from users.models import User


class Task(models.Model):
    name = models.CharField(max_length=100, verbose_name='Task name')
    description = models.TextField(max_length=1000, verbose_name='Task description')
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    deadline = models.DateField()
    status = models.CharField(max_length=100)