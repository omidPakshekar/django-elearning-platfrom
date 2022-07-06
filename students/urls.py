from django.urls import path
from . import views

app_name = 'students'
urlpatterns = [
    path('enroll/', views.StudentEnrollCourseView.as_view(), name='student-enroll'),
    path('courses/', views.StudentCourseListView.as_view(), name='student_course_list'),
    path('course/<int:pk>/', views.StudentCourseDetailView.as_view(), name='student-course-detail'),
    path('course/<int:pk>/module/<int:module_id>/', views.StudentCourseDetailView.as_view(), name='student-course-module-detail'),


]