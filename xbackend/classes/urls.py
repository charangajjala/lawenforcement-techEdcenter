from django.urls import path
from . import views

urlpatterns = [
  #admin classes urls
  path('admin/classes/',views.AdminClassesAPI.as_view(),name='admin_classes'),
  path('admin/classes/<int:id>',views.AdminClassAPI.as_view(),name='admin_class'),
  path('admin/classes/signin/<int:id>',views.AdminStudentSignInAPI.as_view(),name='signin'),
  path('admin/classes/sendEvaluation/<int:id>',views.AdminStudentEvaluationAPI.as_view(),name='evaluation'),
  path('admin/classes/move/<int:id>',views.MoveStudentAPI.as_view(),name='move'),
  path('admin/classes/remove/<int:id>',views.RemoveStudentAPI.as_view(),name='remove'),
  path('admin/classes/substitute/<int:id>',views.SubstituteStudentAPI.as_view(),name='substitute'),
  path('admin/classes/inServiceRoster/<int:id>/',views.AdminInserviceServices.as_view(),name='inservice_classes_alt'),

  #ui classes urls
  path('classes/',views.ClassesAPI.as_view(),name='classes'),
  path('classes/<int:id>/',views.ClassAPI.as_view(),name='class'),
  path('classes/register/verifyAttendee/<int:id>',views.ClassAttendeeVerificationAPI.as_view(),name='attendee_verification'),
  path('classes/register/<int:id>',views.ClassRegisterAPI.as_view(),name='class_registration'),

  #class instructor dashoard urls
  path('classes/instructor/current/',views.InstructorCurrentClassesAPI.as_view(),name='icurrent_cls'),
  path('classes/instructor/past/',views.InstructorPastClassesAPI.as_view(),name='ipast_cls'),
  path('classes/instructor/docs/<int:id>',views.InstructorDocsAPI.as_view(),name='idocs'),
  path('classes/instructor/courseDocs/',views.CourseDocsAPI.as_view(),name='icourse_docs'),
  path('classes/instructor/attendance/<int:id>/',views.AttendanceAPI.as_view(),name='attendance'),
  path('classes/instructor/close/<int:id>',views.CloseClassAPI.as_view(),name='close_cls'),

  #class student dashboard urls
  path('classes/student/current/',views.StudentCurrentClassesAPI.as_view(),name='scurrent_cls'),
  path('classes/student/past/',views.StudentPastClassesAPI.as_view(),name='spast_cls'),
  path('classes/student/tracks/',views.StudentTracksAPI.as_view(),name='stracks'),
  path('classes/student/attendance/<int:id>/',views.StudentAttendanceAPI.as_view(), name='sattendance'),
  path('classes/student/evaluation/<int:id>',views.StudentEvaluationAPI.as_view(), name='sevaluation'),

  #class host urls
  path('classes/host/current/',views.HostCurrentClassesAPI.as_view(),name='hcurrent_cls'),
  path('classes/host/past/',views.HostPastClassesAPI.as_view(),name='hpast_cls'),

  #invoice urls
  #get is done post needs some work
  path('invoice/',views.InvoiceAPI.as_view(),name='invoice'),

  #admin invoice urls
  path('admin/invoice/',views.AdminInvoicesAPI.as_view(),name='admin_invoices'),
  path('admin/invoice/<int:id>',views.AdminInvoiceAPI.as_view(),name='admin_invoice'),
]