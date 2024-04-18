import os

from django.core.management.base import BaseCommand

from users.models import User
from tasks.models import Task
from faker import Faker
import random
from decimal import Decimal

fake = Faker()


class Command(BaseCommand):
    """
        Команда для сброса и добавления тестовых данных в модель Task и User.

        Метод `handle` выполняет следующие шаги:
        1. Удаляет все записи в моделях Payment, Lesson, Course и User.
        2. Создает супер пользователя
        3. Создает 7 пользователей и сохраняет их в список.
        4. Создает 20 задач.

        Attributes:
            help (str): Описание команды для вывода при запуске `python manage.py help`.
    """
    help = 'Reset and add sample payment data to the Payment model'

    def handle(self, *args, **kwargs):

        Task.objects.all().delete()
        User.objects.all().delete()

        user = User.objects.create(
            email='admin@admin.ru',
            first_name='admin',
            last_name='admin',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )

        user.set_password('qwe123rt45')
        user.save()
        print('Create superuser')

        users = []
        for _ in range(7):
            email = fake.email()
            phone = fake.numerify()
            city = fake.city()
            first_name = fake.first_name()
            last_name = fake.last_name()
            user = User.objects.create(email=email, phone=phone, city=city,
                                       first_name=first_name, last_name=last_name)
            user.set_password('qwe123rt45')
            user.save()
            users.append(user)
        print('Add users')

        tasks = []
        for i in range(20):
            task = Task.objects.create(
                name=fake.name(),
                description=fake.text(),
                creator=random.choice(users),
                status=random.choice(['n', 't', 'f', 'd']),
                deadline=fake.date_this_year(before_today=True, after_today=True),
                parent_task=random.choice(tasks) if random.choice([True, False]) and tasks != []
                else None,
            )
            tasks.append(task)
        print('Add tasks')
