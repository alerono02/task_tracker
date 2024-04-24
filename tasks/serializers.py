from django.db.models import Count
from rest_framework import serializers

from tasks.models import Task
from tasks.validators import TaskValidator
from users.models import User
from users.serializers import UserSerializer


class TaskSerializer(serializers.ModelSerializer):
    executor = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        validators = [TaskValidator(field='deadline')]
        order_by = ['id']


class ImportantTaskSerializer(serializers.ModelSerializer):
    free_executor = serializers.SerializerMethodField()
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        validators = [TaskValidator(field='deadline')]

    def get_free_executor(self, obj):
        # obj - 1 task
        executors = User.objects.annotate(task_count=Count('tasks')).order_by('task_count')
        executors = executors.filter(is_superuser=False)
        least_busy_executor = executors.first()
        print(obj.parent_task.executor)
        print(least_busy_executor)
        if obj.parent_task.executor is not None:
            parent_task_executor_tasks = Task.objects.filter(executor_id=obj.parent_task.executor_id,
                                                             status='t').count()
            if parent_task_executor_tasks - least_busy_executor.task_count <= 2:
                return UserSerializer(obj.parent_task.executor).data
        else:
            return UserSerializer(least_busy_executor).data
