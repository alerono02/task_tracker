from django.db import models

from users.models import User


class Task(models.Model):
    STATUS_CHOICES = (
        ('n', 'new'),
        ('t', 'took in work'),
        ('d', 'done'),
        ('f', 'failed'),
    )
    name = models.CharField(max_length=100, verbose_name='Task name')
    description = models.TextField(max_length=1000, verbose_name='Task description')
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Parent task')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    deadline = models.DateField(verbose_name='Deadline')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='n', verbose_name='Status')

    def __str__(self):
        if self.status in ['n', 'f']:
            return f'{self.name}({self.status})'
        else:
            return f'{self.name}({self.status} by {self.user})'

    class Meta:
        verbose_name = 'task'
        verbose_name_plural = 'tasks'
