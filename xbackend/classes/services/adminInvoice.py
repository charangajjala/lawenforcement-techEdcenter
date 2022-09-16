from genericpath import exists
from classes.serializers import AdminInvoiceRequest,AdminInvoiceResponse,AdminInvoiceListResponse
from classes.models import Invoice,Roster,Class, invoice
from students.models import Student
from users.models import User
from meta.models import Address,Contact
from promos.models import Promo

import random
from django.forms.models import model_to_dict

from django.db.models.query_utils import Q
from django.db import IntegrityError, transaction
from django.utils.crypto import get_random_string

from rest_framework.status import *

class AdminInvoicesServices:
  @classmethod
  def getInvoices(cls,user):
    invoiceObjs = Invoice.objects.all()
    # invoiceList =[]
    # for user in User.objects.all().filter(Q(isAdmin=True)|Q(isSuperUser=True)):
    #   for invocie in invoiceObjs:
    #     if invocie.createdBy==user:
    #       invoiceList.append(invocie)
    invoiceObjectsResponse = AdminInvoiceListResponse(invoiceObjs,many=True)
    response,status = invoiceObjectsResponse.data,HTTP_200_OK
    return response,status

  @classmethod
  def createInvoice(cls,data,user):
    invoiceRequest = AdminInvoiceRequest(data=data)
    try:
      if invoiceRequest.is_valid():
        validData = invoiceRequest.validated_data
        #not handled the attendees
        attendees = validData.pop('attendees')
        classId = validData.pop('cls')
        classObj = Class.objects.get(id=classId)
        pmrAddress = validData.pop('pmrAddress',None)
        addressObj = Address.objects.create(**pmrAddress) 
        pmrContact = validData.pop('pmrContact',None)
        contactObj = Contact.objects.create(**pmrContact)
        accessKey = get_random_string(length=15)
        promoId = validData.pop('promoId',None)
        if promoId:
          promoObj = Promo.objects.get(id=promoId)
          invoiceObj = Invoice.objects.create(
            **dict(
              validData,
              promo=promoObj,
              invoiceNum = random.randint(9,99999999),
              accessKey=accessKey,
              pmrAddress=addressObj,
              pmrContact=contactObj,
              createdBy=user
            )
          )
          if promoObj.singleUse == True:
            setattr(promoObj,'isActive',False)
            promoObj.save()
        else:
          print('entered Here')
          invoiceObj = Invoice.objects.create(
            **dict(
              validData,
              invoiceNum = random.randint(9,99999999),
              accessKey=accessKey,
              pmrAddress=addressObj,
              pmrContact=contactObj,
              createdBy=user
            )
          )

        #for attendees in split classes
        if attendees:
          for student in attendees:
            studentObj = Student.objects.get(id=student.id)
            if Roster.objects.get(Q(student=studentObj)&Q(cls=classObj)) == None:
              Roster.objects.create(
                student=studentObj,
                cls=classObj,
                invocie=invoiceObj
              )
        setattr(classObj,'inServiceInvoice',invoiceObj)
        classObj.save()
        # for student in attendees:
        #   studentObj = Student.objects.get(id=student.get('id'))
        #   Roster.objects.create(
        #     student=studentObj,
        #     cls=classObj,
        #     invoice =invoiceObj,
        #   )
        invoiceResponse = AdminInvoiceResponse(invoiceObj,context={'classObj':classObj})
        response,status = invoiceResponse.data,HTTP_200_OK
      else:
        print('Data Invalid',invoiceRequest.errors)
        response,status = invoiceRequest.errors,HTTP_400_BAD_REQUEST
    except User.DoesNotExist:
      response,status = dict(error='Sign Up First'),HTTP_400_BAD_REQUEST
    except Roster.DoesNotExist:
      response,status = dict(error='Roster Object does not exit'),HTTP_400_BAD_REQUEST
    except Roster.MultipleObjectsReturned:
      response,status = dict(error='Multiple roster Not possible'),HTTP_400_BAD_REQUEST
    except Class.DoesNotExist:
      response,status = dict(error='Requested class does not exist'),HTTP_400_BAD_REQUEST
    except Class.MultipleObjectsReturned:
      response,status = dict('Not sure if the requested detials are right'),HTTP_400_BAD_REQUEST
    return response,status        

class AdminInvoiceSerivces:
  @classmethod
  def getInvoice(cls,id):
    invoiceObj = Invoice.objects.get(invoiceNum=id)
    try:
      classObj = Class.objects.get(inServiceInvoice=invoiceObj.id)
    except Class.DoesNotExist:
      rosterObj = Roster.objects.get(invoice=invoiceObj)
      classObj = Class.objects.get(id=rosterObj.cls.id)
    invoiceObjResponse = AdminInvoiceResponse(invoiceObj,context={'classObj':classObj})
    response,status = invoiceObjResponse.data,HTTP_200_OK
    return response,status

  @classmethod
  def updateInvoice(cls,id,data,user):
    invoiceRequest=AdminInvoiceRequest(data=data,partial=True)
    if invoiceRequest.is_valid():
      try:
        validData = invoiceRequest.validated_data
        invoiceObj = Invoice.objects.get(invoiceNum=id)
        oldValues={}
        #dont Know what to do with the attendees
        attendees = validData.pop('attendees',None)
        pmrAddress = validData.pop('pmrAddress',None)
        pmrContact = validData.pop('pmrContact',None)
        try:
          with transaction.atomic():
            if pmrContact:
              contactObj = Contact.objects.create(**pmrContact)
              setattr(invoiceObj,'pmrContact',contactObj)
            if pmrAddress:
              addressObj = Address.objects.create(**pmrAddress) 
              setattr(invoiceObj,'pmrAddress',addressObj)
            print('All Done upto herre')
            for k,v in validData.items():
              oldValues[k] = getattr(invoiceObj,k)
              setattr(invoiceObj,k,v)
            invoiceObj.update(oldValues,currentUser=user)
            invoiceObjResponse = AdminInvoiceResponse(invoiceObj)
            response,status = invoiceObjResponse.data,HTTP_200_OK
        except IntegrityError:
          response,status = dict(error = 'There was error while adding data'),HTTP_400_BAD_REQUEST
      except Invoice.DoesNotExist:
        response,status = dict(error='Check the invoice id again'),HTTP_400_BAD_REQUEST
      except Invoice.MultipleObjectsReturned:
        response,status = dict(error='Multiple Whoa be careful here'),HTTP_400_BAD_REQUEST
      return response,status
        
  @classmethod
  def deleteInvoice(cls,id,user):
    try:
      invoiceObj = Invoice.objects.get(invoiceNum=id)
      try:
        classObj = Class.objects.get(inServiceInvoice=invoiceObj.id)
        if classObj:
          classObj.inServiceInvoice = None
          classObj.save()
      except Class.DoesNotExist or Class.MultipleObjectsReturned:
        pass
      invoiceObj.delete(currentUser=user)
      response,status =dict(message='The invoice has been deleted successfully'),HTTP_200_OK
    except Invoice.DoesNotExist:
      response,status = dict(error ='The Invoice might already been deleted'),HTTP_400_BAD_REQUEST
    except Invoice.MultipleObjectsReturned:
      response,status = dict(error='Not at all possible'),HTTP_400_BAD_REQUEST
    return response,status
