import email
from urllib.request import Request
from students.models import Student
from users.models import User
from classes.serializers import ClassEvaluationRequest
from classes.models import Class,Roster,Evaluation

from django.db import IntegrityError
from django.db.models.query_utils import Q
from django.forms import model_to_dict
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.status import *

class AdminStudentEvaluationSevices:
  @classmethod
  def sendEvaluation(cls,id,data):
    studentId = data.get('studentId')
    studentObj = Student.objects.get(id=studentId)
    subject = 'Police Technical'
    message = 'Please Submit your Evaluation {}'.format(studentObj.user.firstName+studentObj.user.lastName) 
    send_mail(
      subject,
      message,
      settings.EMAIL_HOST_USER,
      [studentObj.user.email,],
      fail_silently=False
    )
    response,status = dict(message = 'Email sent successfully'),HTTP_200_OK
    return response,status

class StudentEvaluationServices:
  @classmethod
  def evaluation(cls,id,data,user):
    evaluationRequest = ClassEvaluationRequest(data=data)
    try:
      if evaluationRequest.is_valid():
        validData = evaluationRequest.validated_data
        evaluationObj = Evaluation.objects.create(**dict(validData))
        classObj = Class.objects.get(id=id)
        studentObj =Student.objects.get(user=user)
        rosterObj = Roster.objects.get(Q(cls=classObj)&Q(student=studentObj))
        setattr(rosterObj,'evaluation',evaluationObj)
        rosterObj.save()
        response,status = dict(message='Evaluation submitted succesfully'),HTTP_200_OK
      else:
        print('Data Invalid')
        response,status = evaluationRequest.errors,HTTP_400_BAD_REQUEST
    except IntegrityError:
      response,status = dict(error = 'Something has other things related'),HTTP_400_BAD_REQUEST
    return response,status
