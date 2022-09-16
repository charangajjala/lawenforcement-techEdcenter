from django.urls import path
from . import views

urlpatterns = [
    path('admin/hours/',views.AdminHoursAPI.as_view(),name='admin_hours')
]
