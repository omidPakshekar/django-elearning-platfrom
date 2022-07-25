
from rest_framework import serializers
from courses.models import Course
from students.models import CustomeUserModel


class StudentInlineSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomeUserModel
        fields = ['email']

class CourseListSeriaLizer(serializers.ModelSerializer):
    students = StudentInlineSerializer(many=True)
    owner = UserSerializer()
    class Meta:
        model = Course
        fields = "__all__"

class CourseCreateSeriaLizer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"