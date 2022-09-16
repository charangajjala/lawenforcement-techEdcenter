from django.urls import path

from . import views

urlpatterns = [
    path('courses/', views.CoursesAPI.as_view(), name='courses'),
    path('courses/<int:id>',views.CourseAPI.as_view(), name='course'),
    path('courses/tracks/',views.TracksAPI.as_view(), name='tracks'),
    path('courses/tracks/<int:id>',views.TrackAPI.as_view(), name='track'),
    path('courses/topics/',views.TopicAPI.as_view(), name='topics'),
    
    path('course/classes/<int:id>/',views.UpcomingClasses.as_view(), name='upcoming_classes'),

    path('admin/courses/', views.AdminCoursesAPI.as_view(), name='admin-courses'),
    path('admin/courses/<int:id>', views.AdminCourseAPI.as_view(), name='admin-course'),
    path('admin/courses/topics/', views.AdminTopicsAPI.as_view(), name='admin-topics'),
    path('admin/courses/topics/<int:id>/', views.AdminTopicAPI.as_view(), name='admin-topic'),
    path('admin/courses/tracks/', views.AdminTracksAPI.as_view(), name='admin-tracks'),
    path('admin/courses/tracks/<int:id>', views.AdminTrackAPI.as_view(), name='admin-track'),
    
    #verify the delete in this url
    path('admin/file/', views.FilesAPI.as_view(), name='file-upload'),

    #ui file upload
    path('file/',views.UiFilesAPI.as_view(),name='ui-file-upload')
]
