"""
  xbackend URL Configuration

"""
#from django.contrib import admin
from django.urls import path, include

#from django.contrib.auth.models import User
#from rest_framework import routers, serializers, viewsets


urlpatterns = [
#    path('admin/', admin.site.urls),
#    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('courses.urls')),
    path('', include('users.urls')),
    path('',include('instructors.urls')),
    path('',include('students.urls')),
    path('',include('hosts.urls')),
    path('',include('classes.urls')),
    path('',include('hours.urls')),
    path('',include('meta.urls')),
    path('',include('promos.urls'))
]
