import pytest
import json

from django.urls import reverse
from rest_framework.status import *
from fixtures import *

from classes.models import Class

@pytest.mark.django_db
class TestAdminClasses:
  def test_post_success(self,adminClient,classValidData):
    response = adminClient.post(reverse('admin_classes'),data=classValidData,format='json')
    resData = json.loads(response.content)
    assert response.status_code == HTTP_201_CREATED
    assert Class.objects.filter(id=resData['id']).exists() == True

  def test_post_unauthorized(self,unauthClient,classValidData):
    response = unauthClient.post(reverse('admin_classes'),data=classValidData,format='json')
    assert response.status_code == HTTP_401_UNAUTHORIZED

  def test_post_forbidden(self,client,classValidData):
    response = client.post(reverse('admin_classes'),data=classValidData,format='json')
    assert response.status_code == HTTP_403_FORBIDDEN

  def test_post_badrequest(self,adminClient,classInvalidData):
    response=adminClient.post(reverse('admin_classes'),data=classInvalidData,format='json')
    assert response.status_code == HTTP_400_BAD_REQUEST

  def test_get_sucess(self,adminClient):
    response = adminClient.get(reverse('admin_classes'))
    resData = json.loads(response.content)
    assert response.status_code == HTTP_200_OK
    assert type(resData) == list

  def test_get_unauthorized(self,unauthClient):
    response = unauthClient.get(reverse('admin_classes'))
    assert response.status_code == HTTP_401_UNAUTHORIZED

  def test_get_forbidden(self,client):
    response = client.get(reverse('admin_classes'))
    assert response.status_code == HTTP_403_FORBIDDEN

@pytest.mark.django_db
@pytest.mark.usefixtures("classId")
class TestAdminClass:
  def test_put_success(self,adminClient,classId):
    response = adminClient.put(
      reverse('admin_class',args=(classId,)),
      data={
        "status":'Booked'
      },
      format='json'
    )
    resData = json.loads(response.content)
    assert response.status_code == HTTP_200_OK
    assert resData.get('status') == 'Booked'
  
  def test_put_unauthorized(self,unauthClient,classId):
    response =unauthClient.put(
      reverse(('admin_class'),args=(classId,)),
      data={
        'status':'Booked'
      },
      format='json'
    )
    assert response.status_code == HTTP_401_UNAUTHORIZED
  
  def test_put_forbidden(self,client,classId):
    response = client.put(
      reverse('admin_class',args=(classId,)),
      data={
        'status':'Booked',
      },
      format='json'
    )
    assert response.status_code == HTTP_403_FORBIDDEN

  def test_put_notfound(self,adminClient,classId):
    response = adminClient.put(
      reverse('admin_class',args=(999,)),
      data = {
        'status':'Booked'
      },
      format='json'
    )
    assert response.status_code == HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestClasses:
  def test_get_success(self,client):
    response = client.get(reverse('classes'),format='json')
    resData = json.loads(response.content)
    assert response.status_code == HTTP_200_OK
    assert type(resData) == list

@pytest.mark.usefixtures("classId")
@pytest.mark.django_db  
class TestClass:
  def test_get_success(self,classId,client):
    response=client.get(reverse('class',args=(classId,)),format='json')
    assert response.status_code == HTTP_200_OK