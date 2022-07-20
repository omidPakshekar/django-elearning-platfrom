
from rest_framework import serializers
from courses.models import Course

class CourseSeriaLizer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"