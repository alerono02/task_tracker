from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
        Права доступа для владельца.

        Владелец имеет право видеть и редактировать свои объекты, а также видеть и редактировать уроки и курсы, если он
        модератор.

        Attributes:
            message (str): Сообщение об ошибке, которое будет возвращено при отсутствии доступа.
    """
    message = "Вы не являетесь создателем."

    def has_object_permission(self, request, view, obj):
        if request.user == obj.creator:
            return True
        return False
