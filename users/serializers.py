from rest_framework import serializers

from tasks.models import Task
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    count_tasks = serializers.SerializerMethodField()

    def get_count_tasks(self, obj):
        return Task.objects.filter(executor_id=obj.id, status='t').count()

    class Meta:
        model = User
        fields = ['id', "count_tasks", 'email', 'password', 'first_name', 'last_name', 'avatar', 'phone', 'city']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return user


# class BusyUserSerializer(serializers.ModelSerializer):
#     count_tasks = serializers.SerializerMethodField()
#
#     def get_count_tasks(self, obj):
#         return Task.objects.filter(executor_id=obj.id, status='t').count()
#
#     class Meta:
#         model = User
#         fields = ('id', 'first_name', 'last_name', 'patronymic', 'email', 'count_tasks')
