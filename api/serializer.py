
from rest_framework import serializers
from courses.models import *
from students.models import CustomeUserModel


class StudentInlineSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomeUserModel
        fields = ['email']

class ModuleListSerializer(serializers.ModelSerializer):    
    contents = serializers.HyperlinkedIdentityField(
        source='contents.all', view_name='api:contents-detail',
        lookup_field='pk', many=True)    
    
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


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"

class ImageSeriaLizer(serializers.ModelSerializer):
    # file = serializers.HyperlinkedIdentityField(
    #         source='modules.all', view_name='api:module-detail',
    #         lookup_field='pk', many=True)
    file = serializers.SerializerMethodField()
    class Meta:
        model = Image
        fields = "__all__"
    def get_file(self, instance):
        # returning image url if there is an image else blank string
        print('hiii', instance.image.url)
        return instance.image.url if instance.image else ''

class VideoSeriaLizer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"


class TextSeriaLizer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = "__all__"

class FileSeriaLizer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"


class ContentListSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField(read_only=True)
    # content = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Content
        fields = "__all__"
    
    def get_content_type(self, obj):
        print(type(obj.item))
        if obj.item._meta.model_name == 'text':
            # print(TextSeriaLizer(obj.item))
            return (TextSeriaLizer(obj.item).data)
        if obj.item._meta.model_name == 'image':
            return ImageSeriaLizer(obj.item).data
        return obj.item._meta.model_name
    # def get_content(self, obj):
    # #     return 