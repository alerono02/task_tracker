from django.http import Http404
from django.utils import timezone
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from permissions import IsOwner
from tasks.paginators import TaskPaginator
from tasks.models import Task
from tasks.serializers import TaskSerializer, ImportantTaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet for TASKS"""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = TaskPaginator

    def perform_create(self, serializer):
        new_task = serializer.save()
        new_task.creator = self.request.user
        new_task.save()

    def check_and_update_task_status(self, task):
        if task.status not in ['d', 'f'] and task.deadline < timezone.now().date():
            task.status = 'f'
            task.save()
            return True
        else:
            return True

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializers = []
        for task in queryset:
            if self.check_and_update_task_status(task):
                serializer = self.get_serializer(task)
                serializers.append(serializer.data)
        return Response(serializers)

    def perform_update(self, serializer):
        task = serializer.save()
        if task.status == 'n' and task.executor is not None:
            task.status = 't'
            task.save()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminUser]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]
        else:
            permission_classes = [IsAuthenticated | IsAdminUser]
        return [permission() for permission in permission_classes]


class ImportantTasks(generics.ListAPIView):
    """
    View for getting important tasks.
    Important tasks are have some params:
    1. not finished or failed tasks
    2. have parent task, which aren't finished or failed
    3. have no executor
    """
    serializer_class = ImportantTaskSerializer

    def get_queryset(self):
        queryset = Task.objects.filter(status='n', parent_task__isnull=False, executor__isnull=True,
                                       parent_task__status__in=['n', 't'])
        return queryset


class TaskTakeView(APIView):
    """
    View for taking tasks
    in url you need write '../take/<id of your task>'
    use POST method
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    # def get_object(self, *args, **kwargs):
    #     if self.request.user.is_authenticated():
    #         try:
    #             task = Task.objects.get(creator=self.request.user)
    #         except:
    #             task = None
    #
    #         if task is None:
    #             HttpResponseRedirect(reverse("task"))
    #
    #     else:
    #         task_id = self.request.session.get("task_id")
    #         if task_id is None:
    #             HttpResponseRedirect(reverse("task"))
    #
    #         task = Task.objects.get(id=task_id)
    #
    #     return task

    def post(self, request, *args, **kwargs):
        user = self.request.user
        task_id = self.kwargs.get('id')

        if task_id is None:
            return Response({"message": "Отсутствует идентификатор задачи в запросе"}, status=400)
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise Http404("Задача с таким идентификатором не найдена")

        if task.executor is None and task.status == 'n':
            task.executor = user
            task.status = 't'
            task.save()
            print(task)
            return Response({"message": "Вы успешно взяли на задачу"}, status=200)
        elif task.executor == user:
            return Response({"message": "Вы уже взяли эту задачу"}, status=400)
        elif task.status != 'n':
            return Response({"message": "Задача не может быть взята в работу"}, status=400)
        else:
            return Response({"message": f"Вы не можете взять задачу. Её выполняет {task.executor}"}, status=400)


class TaskDoneView(APIView):
    """
    View for set done status for your task
    in url you need write '../take/<id of your task>'
    use POST method
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        task_id = self.kwargs.get('id')

        if task_id is None:
            return Response({"message": "Отсутствует идентификатор задачи в запросе"}, status=400)
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise Http404("Задача с таким идентификатором не найдена")

        if task.executor == user and task.status == 't':
            task.status = 'd'
            task.save()
            print(task)
            return Response({"message": "Вы успешно закрыли задачу"}, status=200)
        elif task.executor != user :
            return Response({"message": f"Вы не можете закрыть данную задачу. {task}"}, status=400)
        else:
            return Response({"message": "Задача уже выполнена"}, status=400)