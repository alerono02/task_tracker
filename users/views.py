from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from permissions import IsItMe
from users.models import User
from users.serializers import UserSerializer


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserListAPIView(generics.ListAPIView):
    """View for USER LIST orders by count of tasks"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    ordering = ['-count_tasks']


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """View for USER DETAIL VIEW"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(generics.UpdateAPIView):
    """View for USER UPDATE"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated & IsItMe]


class UserDestroyAPIView(generics.DestroyAPIView):
    """View ro USER DELETE"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated & IsAdminUser]

# class BusyUsers(generics.ListAPIView):
#     serializer_class = BusyUserSerializer
#
#     def get_queryset(self):
#         queryset = User.objects.annotate(task_count=Count('tasks')).order_by('-task_count')
#         return queryset
