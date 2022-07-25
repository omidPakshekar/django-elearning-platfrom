
from rest_framework import serializers
from courses.models import Course, Module
from students.models import CustomeUserModel


class StudentInlineSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomeUserModel
        fields = ['email']

class ModuleListSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Module
        fields = "__all__"

class CourseListSeriaLizer(serializers.ModelSerializer):
    students = StudentInlineSerializer(many=True)
    modules = serializers.HyperlinkedIdentityField(
        source='modules.all', view_name='api:module-detail',
        lookup_field='pk', many=True)    
    owner = UserSerializer()

    class Meta:
        model = Course
        fields = "__all__"

class CourseCreateSeriaLizer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
