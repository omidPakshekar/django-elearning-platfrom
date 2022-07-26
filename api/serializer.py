
from rest_framework import serializers
from courses.models import *
from students.models import CustomeUserModel


class StudentInlineSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)

class ContentInlineSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Content
        fields = ('id', )
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomeUserModel
        fields = ['email']

class ModuleListSerializer(serializers.ModelSerializer):    
    # contents_url = serializers.HyperlinkedIdentityField(
        # source='contents.all', view_name='api:content-detail',
        # lookup_field='pk', many=True)    
    contents = ContentInlineSerializer(many=True)

    class Meta:
        model = Module
        fields = "__all__"

    def update(self,instance,validated_data):
        print('********************', instance.id)
        print('validated_data', (validated_data.keys))
        for attr, value in validated_data.items():
            if not attr == 'contents':
                setattr(instance, attr, value)
        print()
        contents = self.context["request"].data['contents']
        instance.contents
        print(instance.contents.all())
        # for i in contents:

        instance.save()
        print('f', validated_data['contents'][0])
        
        return instance

class CourseListSeriaLizer(serializers.ModelSerializer):
    students = StudentInlineSerializer(many=True)
    modules = serializers.HyperlinkedIdentityField(
        source='modules.all', view_name='api:module-detail',
        lookup_field='pk', many=True)    
    owner = UserSerializer()
    # def get_file(self, obj):
    #     print('f', obj.photo)
    #     return obj.photo.url
    class Meta:
        model = Course
        fields = "__all__"

class CourseCreateSeriaLizer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class ImageSeriaLizer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = Image
        fields = "__all__"
    def get_image_url(self, instance):
        # get request from contentListSeriaLizerClass then create uri 
        request = self.context['contentContext'].get('request')
        return request.build_absolute_uri(instance.image.url)

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
        model_name = obj.item._meta.model_name 
        if model_name == 'text':
            return (TextSeriaLizer(obj.item).data)
        if model_name == 'image':
            return ImageSeriaLizer(obj.item, context={'contentContext' : self.context}).data
        if model_name == 'video':
            return (VideoSeriaLizer(obj.item).data)
        if model_name == 'file':
            return (FileSeriaLizer(obj.item).data)
        
        return obj.item._meta.model_name
