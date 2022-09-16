from rest_framework import serializers
from rest_framework.permissions import AllowAny
from classes.models import Roster
from django.db.models.query_utils import Q
from django.forms import model_to_dict

from collections import OrderedDict

from meta.serializers import GetFieldData
from classes.serializers.instructor import DocResponse
from courses.models import Course
from .evaluation import EvalutionResponse

class StudentCurrentClassResponse(serializers.Serializer):
  id = GetFieldData(lambda obj:obj.cls.id)
  course = GetFieldData(lambda obj:obj.cls.course.title)
  instructor = GetFieldData(lambda obj:(obj.cls.instructor.user.firstName+obj.cls.instructor.user.lastName))
  startDate = GetFieldData(lambda obj:obj.cls.startDate)
  endDate = GetFieldData(lambda obj:obj.cls.endDate)
  startTime = GetFieldData(lambda obj:obj.cls.startTime)
  endTime =GetFieldData(lambda obj:obj.cls.endTime)
  host = GetFieldData(lambda obj:obj.cls.host.name)
  location = GetFieldData(lambda obj:obj.cls.location.name)
  paid = serializers.BooleanField(default=False)
  attendance = serializers.BooleanField(default=False)

  def to_representation(self, instance):
      res = super().to_representation(instance)
      res['invoiceNum']=instance.invoice.invoiceNum
      res['accessKey']=instance.invoice.accessKey
      return res

class CourseMaterialResponse(serializers.Serializer):
  material = DocResponse(many=True,allow_empty=True)

class StudentPastClassResponse(serializers.Serializer):
  id = GetFieldData(lambda obj:obj.id)
  course = GetFieldData(lambda obj:obj.course.title)
  instructor = GetFieldData(lambda obj:(obj.instructor.user.firstName+obj.instructor.user.lastName))
  startDate = GetFieldData(lambda obj:obj.startDate)
  endDate = GetFieldData(lambda obj:obj.endDate)
  startTime = GetFieldData(lambda obj:obj.startTime)
  endTime =GetFieldData(lambda obj:obj.endTime)
  host = GetFieldData(lambda obj:obj.host.name)
  location = GetFieldData(lambda obj:obj.location.name)
  docs = DocResponse(many=True,allow_empty=True,required=False)
  
  def to_representation(self, instance):
      res = super().to_representation(instance)
      user = self.context.get('user')
      rosterObj = Roster.objects.get(Q(student=user)&Q(cls=instance))
      evaluationData = EvalutionResponse(rosterObj.evaluation,context={'studentId':rosterObj.student.id})
      courseObj = Course.objects.get(id=instance.course.id)
      courseMaterial = DocResponse(courseObj.material.all(),many=True,allow_empty=True)
      res['courseMaterials'] = courseMaterial.data
      if evaluationData.data != None:
        res['evaluation'] = evaluationData.data    
      res['attendance'] = rosterObj.attendance  
      res['invoiceNum']=rosterObj.invoice.invoiceNum
      res['accessKey']=rosterObj.invoice.accessKey
      res['paid'] = rosterObj.invoice.paid
      data = OrderedDict([(key,res[key]) for key in res if res[key] is not None])
      return data

class CourseResponse(serializers.Serializer):
  id = serializers.IntegerField()
  title = serializers.CharField()

class CourseCompletionResponse(serializers.Serializer):
  id = serializers.IntegerField()
  title = serializers.CharField()
  
  def to_representation(self, instance):
      res = super().to_representation(instance)
      completedOn = self.context.get('completedOn')
      res['completedOn'] = completedOn
      return res

class RemainingCoursesResponse(serializers.Serializer):
  required = CourseResponse(many=True,allow_empty=True)
  optional = CourseResponse(many=True,allow_empty=True)

class StudentTracksResponse(serializers.Serializer):
  id = serializers.IntegerField()
  title = serializers.CharField()
  shortName = serializers.CharField()

  def to_representation(self, instance):
      res = super().to_representation(instance)
      completedCourses = self.context.get('completed')
      response = CourseCompletionResponse(completedCourses,many=True,context={'completedOn':self.context.get('endDate')})
      remainingRequired = self.context.get('rRemaining')
      remianingOptional = self.context.get('oRemaining')
      remainingCourses = RemainingCoursesResponse({
        'required' : remainingRequired,
        'optional' : remianingOptional
      })
      res['completedCourses'] = response.data
      res['remainingCourses'] = remainingCourses.data
      print('This is the response',res)
      return res
