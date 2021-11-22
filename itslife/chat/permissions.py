from rest_framework import permissions

class IsUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return request.user == obj.user1 or request.user == obj.user2