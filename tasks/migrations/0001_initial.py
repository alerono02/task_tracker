# Generated by Django 4.2.7 on 2024-04-14 08:42

from django.db import migrations, models
import django.db.models.deletion


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
                ('parent_task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tasks.task', verbose_name='Parent task')),
            ],
            options={
                'verbose_name': 'task',
                'verbose_name_plural': 'tasks',
            },
        ),
    ]