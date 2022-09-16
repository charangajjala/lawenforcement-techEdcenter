import re
import pytest
import json

from django.urls import reverse

from rest_framework.status import *

from hosts.models import Location
from fixtures import *

@pytest.mark.django_db
class TestAdminLocation:
  def test_post_success(self,adminClient,locationValidData):
    response = adminClient.post(reverse('admin_locations'),data=locationValidData,format='json')
    resData = json.loads(response.content)
    assert response.status_code == HTTP_201_CREATED
    assert Location.objects.filter(id=resData['id']).exists() == True

  def test_get_success(self,adminClient):
    response = adminClient.get(reverse('admin_locations'),format='json')
    resData = json.loads(response.content)
    assert response.status_code == HTTP_200_OK
    assert type(resData) == list

@pytest.mark.django_db
class TestAdminLocation:
  def test_get_success(self,adminClient,locationId):
    response = adminClient.get(reverse('admin_location',args=(locationId,)),format='json')
    assert response.status_code == HTTP_200_OK
  
  def test_put_success(self,adminClient,locationId):
    response = adminClient.put(
      reverse('admin_location',args=(locationId,)),
      data={
        'seats':512
      },
      format='json'
    )
    resData = json.loads(response.content)
    assert response.status_code == HTTP_200_OK
    assert resData['seats'] == 512
  
  def test_delete_success(self,adminClient,locationId):
    response = adminClient.delete(reverse('admin_location',args=(locationId,)),format='json')
    assert response.status_code == HTTP_200_OK

@pytest.mark.django_db
class TestLocations:
  def test_post_success(self,client,locationValidData):
    response = client.post(reverse('locations'),data=locationValidData,format='json')
    resData = json.loads(response.content)
    assert response.status_code == HTTP_201_CREATED
    assert Location.objects.filter(id=resData['id']).exists() == True

  def test_post_unauthorized(self,unauthClient,locationValidData):
    response = unauthClient.post(reverse('locations'),data=locationValidData,format='json')
    assert response.status_code == HTTP_401_UNAUTHORIZED
  
  def test_post_badrequest(self,client,locationInvalidData):
    response = client.post(reverse('locations'),data=locationInvalidData,format='json')
    assert response.status_code == HTTP_400_BAD_REQUEST

  @pytest.mark.usefixtures('locationId')
  def test_get_success(self,client):
    response = client.get(reverse('locations'), format='json')
    resData = json.loads(response.content)
    assert response.status_code == HTTP_200_OK
    assert type(resData) == list

  @pytest.mark.usefixtures('locationId')
  def test_get_unauthorized(self,unauthClient):
    response = unauthClient.get(reverse('locations'), format='json')
    assert response.status_code == HTTP_401_UNAUTHORIZED  

@pytest.mark.django_db
@pytest.mark.usefixtures('locationId','hostId')
class TestLocation:

  def test_put_success(self,client,locationId):
    response = client.put(
      reverse('location',args=(locationId,)),
      data={
        'seats':154,
      },
      format='json'
    )
    resData = json.loads(response.content)
    assert response.status_code == HTTP_200_OK
    assert resData['seats'] == 154

  def test_put_unauthorized(self,unauthClient,locationId):
    response = unauthClient.put(
      reverse('location',args=(locationId,)),
      data={
        'seats':154,
      },
      format='json'
    )
    assert response.status_code == HTTP_401_UNAUTHORIZED

  def test_put_badrequest(self,client,locationId):
    response = client.put(
      reverse('location',args=(locationId,)),
      data={
        'seats':'Location 2',
      },
      format='json'
    )
    assert response.status_code == HTTP_400_BAD_REQUEST

  def test_get_success(self,client,locationId):
    response = client.get(reverse('location',args=(locationId,)),format='json')
    assert response.status_code == HTTP_200_OK

  def test_get_unauthorized(self,unauthClient,locationId):
    response = unauthClient.get(reverse('location',args=(locationId,)),foramt='json')
    assert response.status_code == HTTP_401_UNAUTHORIZED 