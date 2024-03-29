from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.static import static

urlpatterns = [
    path('', include('homepage.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('courses/', include('courses.urls')),
    path('students/', include('students.urls', namespace='students')),
    path('api/v1/', include('courses.api.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += path('__debug__/', include('debug_toolbar.urls')),
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
