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
        Команда для сброса и добавления тестовых данных в модель Payment.

        Метод `handle` выполняет следующие шаги:
        1. Удаляет все записи в моделях Payment, Lesson, Course и User.
        2. Создает супер пользователя
        3. Создает 5 пользователей и сохраняет их в список.
        4. Создает 5 курсов и для каждого курса создает 3 урока.
        5. Создает 20 случайных платежей, связанных с пользователями, курсами и уроками.

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

        tasks = []
        for i in range(20):
            task = Task.objects.create(
                name=fake.word(),
                description=fake.text(),
                creator=random.choice(users),
            )
            courses.append(course)


        for _ in range(20):
            user = random.choice(users)
            payment_date = fake.date_between(start_date='-30d', end_date='today')
            payment_method = random.choice([1, 2])
            is_course = random.choice([True, False])
            amount = Decimal(random.uniform(1000, 3000))
            course_or_lesson = random.choice(courses) if is_course else random.choice(lessons)

            Payment.objects.create(
                user=user,
                date=payment_date,
                course=course_or_lesson if is_course else None,
                lesson=course_or_lesson if not is_course else None,
                price=amount,
                payment_method=payment_method,
            )