from django import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name='courses'
urlpatterns = [
    path('', views.CourseListView.as_view(), name='course-list'),
    path('mine/', views.CourseListView.as_view(), name='owner-course-list'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('create/', views.CourseCreateView.as_view(), name='create-course' ),
    
]

