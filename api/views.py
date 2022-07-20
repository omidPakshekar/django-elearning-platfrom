from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from .serializer import CourseSeriaLizer
from courses.models import Course

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSeriaLizer