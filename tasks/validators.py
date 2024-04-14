from rest_framework import serializers


class TaskValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        parent_task = dict(value).get(self.field)
        if parent_task and parent_task.status != 'c':
            raise serializers.ValidationError(f'Task {parent_task.name} is not completed yet')
