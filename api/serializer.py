
from rest_framework import serializers
from courses.models import Course


class StudentInlineSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    
class CourseListSeriaLizer(serializers.ModelSerializer):
    
    students = StudentInlineSerializer(many=True)
    class Meta:
        model = Course
        fields = "__all__"

class CourseCreateSeriaLizer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"