from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from django.conf import settings
from django.conf.urls.static import static

from . import views
from . import tokens

urlpatterns = [
    path('admin/users/', views.UsersAPI.as_view(), name='users'),
    path('admin/users/<int:id>/', views.UserAPI.as_view(), name='user'),

    path('users/',views.StandardUserAPI.as_view(),name='standard-user'),
    path('users/team/',views.UserListAPI.as_view(),name='user-list'),
    
    # path('authentication/', jwt_views.TokenObtainPairView.as_view(), name='token-obtain'),
    # path('authentication/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # ui authentication
    # path('authentication/', tokens.get_tokens_for_user, name='token-obtain'),
    path('authentication/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # NTAuthentication
    path('authentication/',tokens.UiTokenObtainPairView.as_view(), name='ui_token'),
    path('admin/authentication/',tokens.AdminTokenObtainPairView.as_view(),name='admin_token_obtain'),

    # admin ui authentication
    # path('admin/authentication/',tokens.get_tokens_for_admin_user,name='admin_token_obtain'),
    path('admin/authentication/refresh/',jwt_views.TokenRefreshView.as_view(),name='admin_token_refresh')
]