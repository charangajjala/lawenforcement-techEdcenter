from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
    path('admin/users/', views.UsersAPI.as_view(), name='users'),
    path('admin/users/<int:id>/', views.UserAPI.as_view(), name='user'),
    
    path('authentication/', jwt_views.TokenObtainPairView.as_view(), name='token-obtain'),
    path('authentication/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
