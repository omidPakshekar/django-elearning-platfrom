from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, viewsets
from .serializer import CourseListSeriaLizer, CourseCreateSeriaLizer
from courses.models import Course

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    
    def get_serializer_class(self):
        if self.action in "list":
            return CourseListSeriaLizer
        return CourseCreateSeriaLizer