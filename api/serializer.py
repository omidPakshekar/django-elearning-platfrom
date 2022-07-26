
from rest_framework import serializers
from courses.models import *
from students.models import CustomeUserModel
from django.shortcuts import get_object_or_404

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
    contents_url = serializers.HyperlinkedIdentityField(
        source='contents.all', view_name='api:content-detail',
        lookup_field='pk', many=True, read_only=True)    
    contents = ContentInlineSerializer(many=True, write_only=True)

    class Meta:
        model = Module
        fields = "__all__"

    def update(self,instance,validated_data):
        """
            for updating module contents 
            we first change content module foreign key to module 5
            then update it
        """
        contents = validated_data.pop('contents')
        content_list = []
        for i in contents:
            content_list.append(get_object_or_404(Content, id=i['id']))
        # change module content to null
        for i in instance.contents.all():
            i.module = Module.objects.get(id=5)
            i.save()
        # add new content to module
        instance.contents.set(content_list) 
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
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
