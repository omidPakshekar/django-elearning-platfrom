from django import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name='courses'
urlpatterns = [
    path('', views.CourseListView.as_view(), name='course-list'),
    # path('test/', views.)
    path('mine/', views.CourseListView.as_view(), name='owner-course-list'),
    path('create/', views.CourseCreateView.as_view(), name='create-course' ),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course-update'),
    path('<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course-delete'),
    path('<int:pk>/modules/', views.CourseModuleListView.as_view(), name='course-module-list'),
    path('<int:pk>/modules/create/', views.CourseModuleCreateView.as_view(), name='course-add-module'),
    path('<int:pk>/modules/<int:module_id>/', views.CourseModuleDetailView.as_view(), name='course-module'),
    path('<int:pk>/modules/<int:module_id>/delete/', views.CourseModuleDeleteView.as_view(), name='course-module-delete'),
    path('<int:pk>/modules/<int:module_id>/update/', views.CourseModuleUpdateView.as_view(), name='course-module-update'),
    # manage content
    path('<int:pk>/modules/<int:module_id>/content/<int:content_id>/delete/', views.ModuleContentDeleteView.as_view(), name='delete-content'),
    path('<int:pk>/modules/<int:module_id>/content/<int:content_id>/update/', views.ModuleContentUpdateView.as_view(), name='update-content'),
    path('<int:pk>/modules/<int:module_id>/model/<str:model_name>/', views.ModuleContentCreateView.as_view(), name='create-content'),

]

