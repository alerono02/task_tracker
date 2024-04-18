from django.utils import timezone
from rest_framework import serializers


class TaskValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        deadline = dict(value).get(self.field)
        if deadline <= timezone.now().date():
            raise serializers.ValidationError('Deadline cannot set earlier than tomorrow!')
