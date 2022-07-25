from django.urls import path, include
from . import views

from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('course', views.CourseViewSet)
router.register('module', views.ModuleViewSet,basename="module")


app_name='api'
urlpatterns = [
    path('',  include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
