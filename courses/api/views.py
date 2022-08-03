from turtle import update
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from rest_framework.decorators import api_view, action 
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions

from .serializer import CourseSeriaLizer, ModuleListSerializer, ContentListSerializer
from courses.models import *
from .permissions import ContentPermission, UserPermission, ModulePermission




class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [UserPermission]

    def get_serializer_class(self):
        # if self.action in ["list"]:
        #     return CourseListSeriaLizer
        return CourseSeriaLizer

    """
        cache list method for 3 minutes
    """    
    @method_decorator(cache_page(180), vary_on_headers('cookie'))
    def list(self, *args, **kwargs):
        return super(CourseViewSet, self).list(*args, **kwargs)

    def put(self, *args, **kwargs):
        print('hi')
        return super(CourseViewSet, self).put(*args, **kwargs)
        

    @action(methods=["get"], detail=False, name="Posts by the logged in user")
    def mine(self, request):
        if request.user.is_anonymous:
            raise PermissionDenied("You must be logged in to see which Posts are yours")
        courses = self.get_queryset().filter(owner=request.user)
        page = self.paginate_queryset(courses)
        if page is not None:
            serializer = CourseSeriaLizer(page, many=True, context={"request": request})
        serializer = CourseSeriaLizer(courses, many=True, context={"request": request})
        return Response(serializer.data)

    @action(methods=["get"], detail=False, name="you join in this course")
    def students(self, request):
        if request.user.is_anonymous:
            raise PermissionDenied("You must be logged in to see which Posts are yours")
        courses = self.get_queryset().filter(students=request.user)
        page = self.paginate_queryset(courses)
        if page is not None:
            serializer = CourseSeriaLizer(page, many=True, context={"request": request})
        serializer = CourseSeriaLizer(courses, many=True, context={"request": request})
        return Response(serializer.data)


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    permission_classes = [ModulePermission]

    def get_serializer_class(self):
        return ModuleListSerializer

class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    permission_classes = [ContentPermission]

    def get_serializer_class(self):
        return ContentListSerializer
