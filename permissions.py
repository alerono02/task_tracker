from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
        Права доступа для владельца.

        Владелец имеет право видеть и редактировать свои объекты, а также видеть и редактировать, если он
        модератор.

        Attributes:
            message (str): Сообщение об ошибке, которое будет возвращено при отсутствии доступа.
    """
    message = "Вы не являетесь создателем или исполнителем задачи!"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.creator or request.user == obj.executor:
            return True
        return False


class IsItMe(BasePermission):
    message = "It's not your account!!"
    def has_object_permission(self, request, view, obj):
        if request.user == obj:
            return True
        return False
