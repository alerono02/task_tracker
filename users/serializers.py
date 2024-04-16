from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'patronymic', 'email', 'position', 'city', 'phone',)


# class BusyUserSerializer(serializers.ModelSerializer):
#     count_tasks = serializers.SerializerMethodField()
#
#     def get_count_tasks(self, obj):
#         return Task.objects.filter(executor_id=obj.id, status='t').count()
#
#     class Meta:
#         model = User
#         fields = ('id', 'first_name', 'last_name', 'patronymic', 'email', 'count_tasks',)
