from rest_framework import permissions

from instructors.models import Instructor,Applicant
from hosts.models import Host
from students.models import Student

#xui roles
class IsInstructor(permissions.BasePermission):

  def has_permission(self, request, view):
      user = request.user
      instructor = Instructor.objects.get(user = user)
      return user or instructor
  
  def has_object_permission(self, request, view, obj):
      user = request.user
      instructor = Instructor.objects.get(user=user)
      return user and instructor
      #return user and instructor.isActive == True

class IsHost(permissions.BasePermission):

  def has_permission(self, request, view):
      user = request.user
      host = Host.objects.get(contactUser=user)
      return user or host
  
  def has_object_permission(self, request, view, obj):
      user = request.user
      host = Host.objects.get(contactUser=user)
      return user and host

class IsStudent(permissions.BasePermission):

  def has_permission(self, request, view):
      user = request.user
      student = Student.objects.get(user=user)
      return user or student

  def has_object_permission(self, request, view, obj):
      user = request.user
      student = Student.objects.get(user = user)
      return user and student

#xadminui roles
class IsAdmin(permissions.BasePermission):

  def has_permission(self, request, view):
      return request.user and request.user.isAdmin

  def has_object_permission(self, request, view, obj):
      return request.user and request.user.isAdmin

class IsSuperUser(permissions.BasePermission):

  def has_permission(self, request, view):
      return request.user and request.user.isSuperUser
  
  def has_object_permission(self, request, view, obj):
      return request.user and request.user.isSuperUser