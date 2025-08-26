from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    """
    Права для модераторов: могут просматривать и редактировать, но не могут создавать и удалять
    """
    def has_permission(self, request, view):
        if request.user.groups.filter(name='moderators').exists():
            if view.action in ['create', 'destroy']:
                return False
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='moderators').exists()


class IsOwner(permissions.BasePermission):
    """
    Права для владельцев объектов: могут работать только со своими объектами
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
