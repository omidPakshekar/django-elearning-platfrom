from django.urls import path
from . import views

app_name = 'students'
urlpatterns = [
    path('enroll/', views.StudentEnrollCourseView.as_view(), name='student-enroll'),
]