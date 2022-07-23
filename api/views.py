from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, viewsets

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from .serializer import CourseListSeriaLizer, CourseCreateSeriaLizer
from courses.models import Course
from .permissions import IsOwnerOrReadOnly
from rest_framework import permissions




class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    # permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CourseListSeriaLizer
        return CourseCreateSeriaLizer

    """
        cache list method for 3 minutes
    """    
    @method_decorator(cache_page(180), vary_on_headers('cookie'))
    def list(self, *args, **kwargs):
        return super(CourseViewSet, self).list(*args, **kwargs)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions per method.
        """
        permission_classes = []
        if self.action in ['create', 'destroy']:
            permission_classes =  [permissions.IsAdminUser]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]
        

