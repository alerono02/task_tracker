# Generated by Django 4.2.7 on 2024-04-14 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Task name')),
                ('description', models.TextField(max_length=1000, verbose_name='Task description')),
                ('deadline', models.DateField(verbose_name='Deadline')),
                ('status', models.CharField(choices=[('n', 'new'), ('t', 'took in work'), ('d', 'done'), ('f', 'failed')], default='n', max_length=1, verbose_name='Status')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateField(auto_now=True, verbose_name='Updated at')),
            ],
            options={
                'verbose_name': 'task',
                'verbose_name_plural': 'tasks',
            },
        ),
    ]