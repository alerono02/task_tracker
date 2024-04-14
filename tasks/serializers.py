from tasks.models import Task
from tasks.validators import TaskValidator


class TaskSerializer:
    class Meta:
        model = Task
        fields = '__all__'
        validators = [TaskValidator(field='parent_task')]
