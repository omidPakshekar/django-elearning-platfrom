
from rest_framework import serializers
from courses.models import Course


class StudentInlineSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    
class CourseSeriaLizer(serializers.ModelSerializer):
    
    students = StudentInlineSerializer(many=True)
    class Meta:
        model = Course
        fields = "__all__"