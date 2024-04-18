from django.db import models

from config import settings
from users.models import User


class Task(models.Model):
    """
    Model for Tasks
    name(str) - title of task
    description(str) - description of task
    parent_task(Task) - parent task
    user(User) - user who will need to complete the task
    deadline(date) - deadline of task
    status(str) - status of task (new, took in work, done or failed)
    creator(User) - user who created the task
    """
    STATUS_CHOICES = (
        ('n', 'new'),
        ('t', 'took in work'),
        ('d', 'done'),
        ('f', 'failed'),
    )
    name = models.CharField(max_length=100, verbose_name='Task name')
    description = models.TextField(max_length=1000, verbose_name='Task description')
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Parent task')
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Executor',
                                 related_name='tasks')
    deadline = models.DateField(verbose_name='Deadline')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='n', verbose_name='Status')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name='Creator',
                                related_name='creator')
    created_at = models.DateField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateField(auto_now=True, verbose_name='Updated at')

    def __str__(self):
        if self.status in ['n', 'f']:
            return f'{self.name}({self.status})'
        else:
            return f'{self.name}({self.status} by {self.executor})'

    class Meta:
        verbose_name = 'task'
        verbose_name_plural = 'tasks'
