from django.db import models
from django.conf import settings


class Subject(models.Model):
    title       = models.CharField(max_length=50)
    slug    = models.SlugField(max_length = 200, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title



class Course(models.Model):
    owner   = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'courses_created', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE)
    title   = models.CharField(max_length=100)
    slug    = models.SlugField(max_length=200, unique=True)
    overview= models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='course_joined', blank=True)
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title