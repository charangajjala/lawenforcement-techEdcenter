from . import views
from django.urls import path


urlpatterns = [
    path('admin/instructors/', views.AdminInstructorsAPI.as_view(), name='admin_instructors'),
    path('admin/instructors/<int:id>/', views.AdminInstructorAPI.as_view(),name='admin_instructor'),
    path('admin/instructors/applicants/',views.AdminInstructorApplicantsAPI.as_view(), name='instructor_applicants'),
    path('admin/instructors/applicants/<int:id>',views.AdminInstructorApplicantAPI.as_view(), name='instructor_applicant'),

    path('instructors/',views.InstructorAPI.as_view(), name='instructor_profile'),
    path('instructors/<int:id>',views.InstructorDetails.as_view(),name='instructor_details'),
    path('instructors/team/',views.InstructorListAPI.as_view(),name='instructor-list'),
    path('instructors/applicants/',views.InstructorApplicantsAPI.as_view(),name='applicant'),
    
#    path('admin/instructors/applicants/', jwt_views.TokenObtainPairView.as_view(), name='token-obtain'),
#    path('admin/instructores/applicants/<int:id>', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
