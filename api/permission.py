from rest_framework.permissions import BasePermission


class IsDirectorOrManager(BasePermission):

    def has_permission(self, request, view):
        if request.user.status == 'director' or request.user.status == 'manager' or request.user.status == 'admin':
            return True
        elif request.method == 'GET':
            return True
        return False


class IsManager(BasePermission):

    def has_permission(self, request, view):
        if request.user.status == 'manager' or request.user.status == 'admin':
            return True
        return False


class IsDirector(BasePermission):

    def has_permission(self, request, view):
        if request.user.status == 'director' or request.user.status == 'admin':
            return True
        return False


class IsOwnerOfTask(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.boss == request.user or request.user.status == 'admin':
            return True
        return False


class IsOwnerOfReview(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user or request.user.status == 'admin':
            return True
        return False


class IsBossOrWorker(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.boss == request.user or obj.worker == request.user or request.user.status == 'admin':
            return True
        return False


class IsAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.boss == request.user or request.user.status == 'admin':
            return True
        return False
