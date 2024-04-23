from django.urls import path
from rest_framework.routers import DefaultRouter

from tasks.apps import TasksConfig
from tasks.views import TaskViewSet, ImportantTasks, TaskTakeView, TaskDoneView

app_name = TasksConfig.name

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('tasks/important/', ImportantTasks.as_view(), name='important_tasks'),
    path('tasks/take/<int:id>', TaskTakeView.as_view(), name='take_task'),
    path('tasks/done/<int:id>', TaskDoneView.as_view(), name='complete_task'),
] + router.urls
