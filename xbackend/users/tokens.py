from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view

from django.http import JsonResponse
from django.contrib.auth.models import update_last_login
from rest_framework.status import *

import jwt

from users.models import User
from students.models import Student
from instructors.models import Instructor
from hosts.models import Host

from rest_framework_simplejwt.settings import api_settings

from django.db.models.query_utils import Q

from rest_framework.status import *
from rest_framework.response import Response

#new modules for authentication process
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

@api_view(['POST'])
def get_tokens_for_user(request):
  data = request.data
  roles=[]
  user = User.objects.get(email=data.get('email').strip())
  
  try: 
    if Student.objects.get(user=user):
      roles.append('student')
  except Student.DoesNotExist:
    pass

  try:
    if Instructor.objects.get(user=user):
      roles.append('instructor')
  except Instructor.DoesNotExist:
    pass

  try:
    if Host.objects.get(contactUser=user):
      roles.append('host')
  except Host.DoesNotExist:
    pass
  
  refresh = RefreshToken.for_user(user)
  return Response({
    'refresh':str(refresh),
    'access':str(refresh.access_token),
    'user':{'roles':roles,'firstName':user.firstName}
  })

@api_view(['POST'])
def get_tokens_for_admin_user(request):
  data = request.data
  try:
    user = User.objects.get(Q(email=data.get('email').strip())&Q(isAdmin=True))
    roles=[]
    if user.isAdmin:
      roles.append('admin')
    else:
      if user.isSuperUser:
        if len(roles) == 0:
          roles.append('superuser')
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh':str(refresh),
      'access':str(refresh.access_token),
      'user':{'roles':roles,'firstName':user.firstName}
    })
  except User.DoesNotExist:
    response,status = dict(error='User does not exist with  email'),HTTP_401_UNAUTHORIZED
    return JsonResponse(response,status=status)


#new authentication process
class UiTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        roles=[]
        user = User.objects.get(email=self.user.email)
        try: 
          if Student.objects.get(user=user):
            roles.append('student')
        except Student.DoesNotExist:
          pass

        try:
          if Instructor.objects.get(user=user):
            roles.append('instructor')
        except Instructor.DoesNotExist:
          pass

        try:
          if Host.objects.get(contactUser=user):
            roles.append('host')
        except Host.DoesNotExist:
          pass
        
        data['user']={'roles':roles,'firstName':user.firstName}

        return data


class UiTokenObtainPairView(TokenObtainPairView):
    serializer_class = UiTokenObtainPairSerializer


class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        user = User.objects.get(Q(email=self.user.email)&Q(isAdmin=True))

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        roles=[]
        if user.isAdmin:
          roles.append('admin')
        else:
          if user.isSuperUser:
            if len(roles) == 0:
              roles.append('superuser')
        refresh = RefreshToken.for_user(user)
        
        data['user']={'roles':roles,'firstName':user.firstName}

        return data


class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer