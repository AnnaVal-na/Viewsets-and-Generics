from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """
    Права для модераторов: могут просматривать и редактировать, но не могут создавать и удалять
    """

    def has_permission(self, request, view):
        if request.user.groups.filter(name="moderators").exists():
            if view.action in ["create", "destroy"]:
                return False
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name="moderators").exists()


class IsOwner(permissions.BasePermission):
    """
    Права для владельцев объектов: могут работать только со своими объектами
    Разрешены методы: GET, PUT, PATCH, DELETE (но не CREATE)
    """

    def has_permission(self, request, view):
        # Владелец может выполнять любые действия кроме создания (create)
        # CREATE обрабатывается отдельно через perform_create
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Явная проверка методов: разрешены GET, PUT, PATCH, DELETE
        if request.method in permissions.SAFE_METHODS + ("PUT", "PATCH", "DELETE"):
            return obj.owner == request.user
        return False
