from django.contrib import admin

from tasks.models import Task
from users.models import User

# Register your models here.
admin.site.register(User)
admin.site.register(Task)