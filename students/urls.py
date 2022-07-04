from django.urls import path
from . import views

app_name = 'students'
urlpatterns = [
    path('enroll/', views.StudentEnrollCourseView.as_view(), name='student-enroll'),
    # path('course/<int:pk>/', views.StudenCourseDetailView.as_view(), name='student_course_detail'),

]