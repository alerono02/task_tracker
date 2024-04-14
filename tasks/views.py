from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.db.models import Q, Count

from permissions import IsOwner
from users.models import User
from users.serializers import UserSerializer
from tasks.models import Task
from tasks.serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        new_task = serializer.save()
        new_task.owner = self.request.user
        new_task.save()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated & (IsAdminUser or IsOwner)]


class ImportantTasks(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.filter(Q(parent_task__isnull=True) & Q(User__isnull=True)).annotate(
            dependent_tasks=Count('task')
        ).filter(dependent_tasks__gt=0)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        least_loaded_User = User.objects.annotate(task_count=Count('task')).order_by('task_count')[0]
        for task in serializer.data:
            users = User.objects.filter(Q(task__parent_task=task.parent_task) | Q(task=task.parent_task))
            if len(users) == 1 and users[0] != task.User:
                task['User'] = UserSerializer(users[0]).data
            elif task.User is None and len(users) < 3 and \
                    User.objects.exclude(id=task.User.id).aggregate(task_count=Count('task'))[
                        'task_count'] <= least_loaded_User.task_count + 2:
                task['User'] = UserSerializer(users[0]).data
        return Response(serializer.data)
