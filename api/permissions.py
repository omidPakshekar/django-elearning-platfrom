from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Instance must have an attribute named `owner`.
        return obj.owner == request.user


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['list', 'mine']:
            return True
        elif view.action == 'create':
            if request.user.is_anonymous:
                return False
            return  request.user.is_staff
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False
                                                                                                
    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        # if not request.user.is_authenticated():
        #     return False
        if view.action == 'retrieve':
            return True
        elif view.action in ['update', 'partial_update']:
            if request.user.is_anonymous:
                return False
            return obj.owner == request.user or request.user.is_admin
        elif view.action == 'destroy':
            if request.user.is_anonymous:
                return False
            return request.user.is_admin
        else:
            return False