from django.urls import path
from . import views

urlpatterns = [
  path('admin/students/',views.AdminStudentsAPI.as_view(),name='admin_students'),
  path('admin/students/<int:id>',views.AdminStudentAPI.as_view(),name='admin_student'),
  path('students/',views.StandardStudentsAPI.as_view(),name='student'),
  path('students/<int:id>',views.StudentDetailsAPI.as_view(),name='student_details')
]