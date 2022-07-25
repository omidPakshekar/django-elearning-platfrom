from django.db import models
from django.conf import settings
from .fields import OrderField
from django.contrib.contenttypes.fields import ContentType, GenericForeignKey

from versatileimagefield.fields import VersatileImageField, PPOIField


User = settings.AUTH_USER_MODEL


def get_course_image_filepath(self, filename):
    return f'courses/{self.title + ".png"}'

def get_default_image():
    return "courses/default_image.jpg"


class Category(models.Model):
    title       = models.CharField(max_length=50, db_index=True)
    slug        = models.SlugField(max_length = 200, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


    
class Course(models.Model):
    owner     = models.ForeignKey(User, related_name = 'courses_created', on_delete=models.CASCADE)
    category  = models.ForeignKey(Category, related_name='courses', on_delete=models.CASCADE)
    # image     = VersatileImageField(ppoi_field="ppoi", upload_to=get_course_image_filepath, null=True, blank=True, default=get_default_image )
    # ppoi      = PPOIField(null=True, blank=True)
    photo     = models.ImageField(upload_to=get_course_image_filepath, null=True, blank=True, default=get_default_image )
    title     = models.CharField(max_length=100)
    slug      = models.SlugField(max_length=200, unique=True)
    overview  = models.TextField()
    created   = models.DateTimeField(auto_now_add=True, db_index=True)
    students  = models.ManyToManyField(User, related_name='course_joined', blank=True)
    
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

class Module(models.Model):
    course      = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title       = models.CharField(max_length=200)
    description = models.TextField(blank = True)
    order       = OrderField(blank=True, for_fields=['course'], db_index=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)


class Content(models.Model):
    class Meta:
        ordering = ['order']

    module      = models.ForeignKey(Module, related_name='contents' , on_delete=models.CASCADE)
    order       = OrderField(blank=True, for_fields=['module'])
    content_type= models.ForeignKey(ContentType,
                                limit_choices_to = {
                                    'model__in':('text', 'video', 'image', 'file')
                                    },
                                on_delete=models.CASCADE)
    object_id   = models.PositiveIntegerField()
    item        = GenericForeignKey('content_type', 'object_id')

    

class ItemBase(models.Model):
    owner       = models.ForeignKey(User, related_name="%(class)s_related", on_delete=models.CASCADE)
    title       = models.CharField(max_length = 250, blank=True)
    created_time= models.DateTimeField(auto_now_add = True)
    updated_time= models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    
class Text(ItemBase):
    content     = models.TextField(blank=True)

class Image(ItemBase):
    image       = models.ImageField(upload_to= 'images')
    # placeholder = models.CharField(max_length=40)

class File(ItemBase):
    file     = models.FileField(upload_to = 'file')

class Video(ItemBase):
    url         = models.URLField()
