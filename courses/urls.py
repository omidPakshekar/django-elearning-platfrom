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
    # path('category/<str:category>/', views.CourseListView.as_view(), name='category-course'),
    path('create/', views.CourseCreateView.as_view(), name='create-course' ),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course-update'),
    path('<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course-delete'),

    
]

