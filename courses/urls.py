from django import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name='courses'
urlpatterns = [
    path('', views.CourseListView.as_view(), name='course-list'),
    path('mine/', views.CourseListView.as_view(), name='test'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
]

