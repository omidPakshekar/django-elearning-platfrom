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
    """
        Deny create actions on objects if the user is not admin
    """ 
    def check_admin_or_staff(request):
        return request.user.is_admin or request.user.is_staff

    def has_permission(self, request, view):
        if view.action in ['list', 'mine', 'students']:
            return True
        elif view.action == 'create':
            if request.user.is_anonymous:
                return False
            return  request.user.is_admin or request.user.is_staff
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False
                                                                                                
    def has_object_permission(self, request, view, obj):
        # if not request.user.is_authenticated():
        #     return False
        if view.action == 'retrieve':
            return True
        elif view.action in ['update', 'partial_update']:
            if request.user.is_anonymous:
                return False
            return obj.owner == request.user or request.user.is_admin or request.user.is_staff
        elif view.action == 'destroy':
            if request.user.is_anonymous:
                return False
            return request.user.is_admin or request.user.is_staff
        else:
            return False


class ModulePermission(UserPermission):
    """
        this class extends from userPermission
    """                                                         
    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        elif view.action in ['update', 'partial_update']:
            if request.user.is_anonymous:
                return False
            return obj.course.owner == request.user or request.user.is_admin
        elif view.action == 'destroy':
            if request.user.is_anonymous:
                return False
            return request.user.is_admin
        else:
            return False

class ContentPermission(permissions.BasePermission):
    """
        create      --> user muust be staff
        list        --> user must be admin
        update      --> user must be owner of course or staff       
        retreive --> user must be student or admin or owner
    """                                                         
    def is_owner(self, request, obj):
        return request.user == obj.module.course.owner
    
    def is_student(self, request, obj):
        return request.user in obj.module.course.students.all()
    
    def has_permission(self, request, view):
        if view.action in ['list']:
            if request.user.is_anonymous:
                return False
            return request.user.is_staff
        elif view.action == 'create':
            if request.user.is_anonymous:
                return False
            return  request.user.is_staff
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False
                                                                                                
    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            if request.user.is_anonymous:
                return False
            return self.is_student(request, obj) or self.is_owner(request, obj) or request.user.is_admin
        elif view.action in ['update', 'partial_update']:
            if request.user.is_anonymous:
                return False
            return self.is_owner(request, obj) or request.user.is_staff
        elif view.action == 'destroy':
            if request.user.is_anonymous:
                return False
            return request.user.is_admin
        else:
            return False
