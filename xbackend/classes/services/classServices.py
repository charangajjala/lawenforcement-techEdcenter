from rest_framework.status import *

from collections import OrderedDict
from promos.models import Promo

from users.models import User
from classes.models import Class
from hosts.models import Host
from meta.models import Address,Contact
from students.models import Student
from classes.models import Roster
from classes.serializers import *
from instructors.models import Instructor
from students.services import StandardStudentServices

from django.utils.crypto import get_random_string
from django.db.models.query_utils import Q

import datetime
import random

class ClassService:

  @classmethod
  def getAll(cls,params):
    try:
      today = datetime.datetime.now().date()
      if params:
        classObjs = Class.objects.all().exclude(type__in=[2,5]).order_by('startDate')
        classObjs = classObjs.exclude(startDate__lt=today)
        courseId = params.get('scourse',None)
        hostId = params.get('shost',None)
        instructorId = params.get('sinstructor',None)
        locationId = params.get('slocation',None)
        month = params.get('smonth',None)
        state = params.get('sstate',None)
        if courseId:
          courseObj = Course.objects.get(id=courseId)
          classObjs = classObjs.filter(course=courseObj)
        if hostId:
          hostObj = Host.objects.get(id=hostId)
          classObjs = classObjs.filter(host=hostObj)
        if instructorId:
          instructorObj = Instructor.objects.get(id=instructorId)
          classObjs = classObjs.filter(instructor=instructorObj)
        if locationId:
          locationObj = Location.objects.get(id=locationId)
          classObjs = classObjs.filter(location=locationObj)
        if state:
          pass
        if month:
          pass
      else:
        classObjs = Class.objects.all().exclude(type__in=[2,5]).order_by('startDate').exclude(startDate__lt=today)
      classResponse = ClassesResponse(classObjs,many=True)
      response,status = classResponse.data,HTTP_200_OK
        
    except ValueError:
        response,status = dict(error = "There is some error that i dont know"), HTTP_404_NOT_FOUND

    return response, status

  @classmethod
  def getClass(cls,id):
    try:
      iclass = Class.objects.get(id=id)
      iclassResponse = ClassResponse(iclass)
      response,status = iclassResponse.data,HTTP_200_OK
    except Class.MultipleObjectsReturned:
      response, status = dict(error = "Multiple classes found"), HTTP_400_BAD_REQUEST
    except Class.DoesNotExist:
      response, status = dict(error = "Class not found"), HTTP_404_NOT_FOUND

    return response,status

  @classmethod
  def getCurrentClasses(cls,user):
    try:
      studentObj = Student.objects.get(user=user)
      rosterObjs = Roster.objects.filter(student=studentObj)
      currentClassObjs = []

      for rosterObj in rosterObjs:
        classObj = rosterObj.get('cls')
        classEndDate = classObj.get('endDate')
        classEndTime = classObj.get('endTime')

        classDay = datetime.datetime.combine(classEndDate,classEndTime)
        today = datetime.datetime.now()
        if classDay>=today:
          currentClassObjs.append(classObj)        

      currentClasses = CurrentClassesResponse(currentClassObjs,many=True)
      response,status = currentClasses.data,HTTP_200_OK
      
    except Student.DoesNotExist:
      response,status = dict(error = 'You are not supposed to be here'),HTTP_400_BAD_REQUEST
    except Student.MultipleObjectsReturned:
      response,status = dict(error = 'This user is getting too much attention'),HTTP_400_BAD_REQUEST

    return response,status

  @classmethod
  def getPastClasses(cls,user):
    try:
      studentObj = Student.objects.get(user=user)
      rosterObjs = Roster.objects.filter(student=studentObj)
      pastClassObjs = []

      for rosterObj in rosterObjs:
        classObj = rosterObj.get('cls')
        classEndDate = classObj.get('endDate')
        classEndTime = classObj.get('endTime')

        classDay = datetime.datetime.combine(classEndDate,classEndTime)
        today = datetime.datetime.now()
        if classDay<=today:
          pastClassObjs.append(classObj)        

      print('Number of current classes are : ',len(pastClassObjs))
      currentClasses = PastClassesResponse(pastClassObjs,many=True)
      response,status = currentClasses.data,HTTP_200_OK
      
    except Student.DoesNotExist:
      response,status = dict(error = 'You are not supposed to be here'),HTTP_400_BAD_REQUEST
    except Student.MultipleObjectsReturned:
      response,status = dict(error = 'This user is getting too much attention'),HTTP_400_BAD_REQUEST

    return response,status

class ClassRegistrationService:
  @classmethod
  def register(cls,id,data):
    registrationRequest = ClassRegistrationRequest(data=data)
    if registrationRequest.is_valid():
      try:
        validData = registrationRequest.validated_data
        accessKey = get_random_string(length=15)

        contact = validData.pop('pmrContact',None)
        contactObj = Contact.objects.create(**contact) if contact else None
        address = validData.pop('pmrAddress',None)
        addressObj = Address.objects.create(**address) if address else None
        student_list = validData.pop('attendees',None)
        print(student_list)
        promoId = validData.pop('promoId',None)
        totalPrice = validData.pop('totalPrice',None)
        #attendees = list(OrderedDict.fromkeys(student_list))
        
        classObj = Class.objects.get(id=id)

        #fee calculation
        earlyFee = classObj.earlyFee
        regularFee = classObj.regularFee
        lateFee = classObj.lateFee
        today = datetime.datetime.now()
        classStart = datetime.datetime.combine(classObj.startDate,classObj.startTime)
        difference = classStart - today
        if classStart > today:
          if difference.days >= 90:
            fee = earlyFee
          if 30<=difference.days<90:
            fee = regularFee
          if 0<=difference.days<30:
            fee = lateFee
        else:
          fee = lateFee
        
        #verify promo
        paymentType = validData.pop('paymentMethod')
        if paymentType == 'Credit Card':
          if promoId:
            promoObj = Promo.objects.get(id=promoId)
            if promoObj.singleUse:
              setattr(promoObj,'isActive',False)
              promoObj.save()
            invoiceObj = Invoice.objects.create(
              **dict(
                validData,
                promo = promoObj,
                invoiceNum = random.randint(9,99999999),
                accessKey = accessKey,
                paymentMethod=1,
                paid=True,
                pmrAddress = addressObj,
                pmrContact = contactObj,
                price=fee,
                totalPrice=totalPrice
              )
            )
          else:
            invoiceObj = Invoice.objects.create(
              **dict(
                validData,
                invoiceNum = random.randint(9,99999999),
                accessKey = accessKey,
                paymentMethod=1,
                paid=True,
                pmrAddress = addressObj,
                pmrContact = contactObj,
                price=fee,
                totalPrice=totalPrice
              )
            )
        else:
          if promoId:
            promoObj = Promo.objects.get(id=promoId)
            if promoObj.singleUse:
              setattr(promoObj,'isActive',False)
            invoiceObj = Invoice.objects.create(
              **dict(
                validData,
                promo=promoObj,
                invoiceNum = random.randint(9,99999999),
                accessKey = accessKey,
                paymentMethod=2,
                paid=False,
                pmrAddress = addressObj,
                pmrContact = contactObj,
                price=fee,
                totalPrice=totalPrice
              )
            )
            promoObj.save()
          else:
            invoiceObj = Invoice.objects.create(
              **dict(
                validData,
                invoiceNum = random.randint(9,99999999),
                accessKey = accessKey,
                paymentMethod=2,
                paid=False,
                pmrAddress = addressObj,
                pmrContact = contactObj,
                price=fee,
                totalPrice=totalPrice
              )
            )
        for student in student_list:
          if type(student) != int:
            addressObj = Address.objects.create(
              address1= student.get('address'),
              address2= student.get('address2'),
              city= student.get('city'),
              state= student.get('state'),
              zip= student.get('zip'),
            )
            userObj = User.objects.create(
              title=student.get('title'),
              firstName = student.get('firstName'),
              lastName = student.get('lastName'),
              email = student.get('email'),
              phone = student.get('phone'),
              address = addressObj,
            )
            studentObj = Student.objects.create(
              user=userObj,
              agencyName = student.get('agency'),
              isActive=True,
            )
          else:
            studentObj = Student.objects.get(id=student)
          Roster.objects.create(
            student = studentObj,
            invoice = invoiceObj,
            cls = classObj,
          )
          print('Roster is genarated for ',studentObj.user.firstName)
        registrationResponse = ClassRegistrationResponse(invoiceObj)
        response,status = registrationResponse.data,HTTP_201_CREATED

      except Class.DoesNotExist:
        response,status = dict(error = 'The class you are looking for does nor exist'),HTTP_400_BAD_REQUEST
      except Class.MultipleObjectsReturned:
        response,status = dict(error = 'Thats not possible'),HTTP_400_BAD_REQUEST
      except Student.DoesNotExist:
        res,stat = StandardStudentServices.createStudent(student)
        id = res.userId
        studentObj = User.objects.get(id=id)
        Roster.objects.create(
          student = studentObj,
          invoice = invoiceObj,
          cls = classObj
        )
        registrationResponse = ClassRegistrationResponse(invoiceObj)
        response,status = registrationResponse.data,HTTP_201_CREATED
      except Student.MultipleObjectsReturned:
        response,status = dict(error = 'The student id has multiple returns'),HTTP_400_BAD_REQUEST
      return response,status

class AttendeeVerification:

  @classmethod
  def verfiy(cls,data,id):
    verificationRequest = ClassAttendeeVerificationRequest(data=data)
    if verificationRequest.is_valid():
      validData=verificationRequest.validated_data
      email=validData.pop('email',None)
      try:
        userObj = User.objects.get(email=email)
        studentObj = Student.objects.get(user=userObj)
        classObj = Class.objects.get(id=id)

        rosterObj = Roster.objects.get(Q(student = studentObj) & Q(cls = classObj))
        studentResponse = ClassAttendeeVerificationResponse(studentObj,context={'rosterObj':rosterObj})
        response,status = studentResponse.data,HTTP_200_OK
      except User.DoesNotExist:
        response,status = dict(error = "No user exists with the given email sign up first"),HTTP_400_BAD_REQUEST
      except User.MultipleObjectsReturned:
        response,status = dict(error =  'Multiple users have the same mail ID'),HTTP_400_BAD_REQUEST
      except Student.DoesNotExist:
        response,status = dict(error = "Gotcha you are not a student"),HTTP_400_BAD_REQUEST
      except Student.MultipleObjectsReturned:
        response,status = dict(error = 'Multiple students found'),HTTP_400_BAD_REQUEST
      except Roster.DoesNotExist:
        if Roster.objects.filter(student = studentObj).exists():
          response,status = dict(error = 'You are registered in other classes but not this'),HTTP_400_BAD_REQUEST
        studentResponse = ClassAttendeeVerificationResponse(studentObj)
        response,status = studentResponse.data,HTTP_200_OK
      except Roster.MultipleObjectsReturned:
        response,status = dict(error = "This cant be happening absolutely"),HTTP_400_BAD_REQUEST
      return response,status