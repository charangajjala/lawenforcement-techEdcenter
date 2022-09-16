from django.http import response
from instructors.models import *
from fixtures import *
import pytest
import json
import io

from django.urls import reverse
from django.core.files import File
from rest_framework.status import *


@pytest.mark.django_db
class TestInstructorAPI:
  def test_put_success(self,client2):
    response = client2.put(
        reverse('instructor_profile'),
        data = { 'ssn' : 'ss2' },
        format = 'json'
    )
    print(client2)
    resData = json.loads(response.content)
    assert response.status_code == HTTP_200_OK


  def test_put_unauthorized(self, unauthClient):
    response = unauthClient.put(
        reverse('instructor_profile'),
        data = { 'ssn' : 'ss2' },
        format = 'json'
    )
    assert response.status_code == HTTP_401_UNAUTHORIZED

  def test_put_notfound(self, client):
    response = client.put(
        reverse('instructor_profile'),
        data = { 'name' : 'Computer & Thinking edited' },
        format = 'json'
    )
    assert response.status_code == HTTP_404_NOT_FOUND

  def test_get_success(self, client2):
    response = client2.get(reverse('instructor_profile'))
    resData = json.loads(response.content)
    assert response.status_code == HTTP_200_OK

  def test_get_unauthorized(self, unauthClient):
    response = unauthClient.get(reverse('instructor_profile'))
    assert response.status_code == HTTP_401_UNAUTHORIZED

  def test_get_notfound(self, client):
    response = client.get(reverse('instructor_profile'))
    resData = json.loads(response.content)
    assert response.status_code == HTTP_404_NOT_FOUND

  def test_get_detail_success(self,client,instructorId):
    response = client.get(reverse('instructor_details',args=(instructorId,)),format='json')
    assert response.status_code == HTTP_200_OK

@pytest.mark.django_db
class TestAdminInstructorAPI:
  def test_put_success(self,adminClient,instructorId):
    response = adminClient.put(
        reverse('admin_instructor', args=(instructorId,)),
        data = { 'ssn' : 'ss2' },
        format = 'json'
    )
    resData = json.loads(response.content)
    assert response.status_code == HTTP_200_OK
    assert Instructor.objects.get(id=instructorId).ssn == 'ss2'

  def test_put_unauthorized(self, unauthClient,instructorId):
    response = unauthClient.put(
        reverse('admin_instructor', args=(instructorId,)),
        data = { 'ssn' : 'ss2' },
        format = 'json'
    )
    assert response.status_code == HTTP_401_UNAUTHORIZED

  def test_put_forbidden(self, client,instructorId):
    response = client.put(
        reverse('admin_instructor', args=(instructorId,)),
        data = { 'ssn' : 'ss2' },
        format = 'json'
    )
    assert response.status_code == HTTP_403_FORBIDDEN


  def test_put_notfound(self, adminClient):
    response = adminClient.put(
        reverse('admin_instructor', args=(999999,)),
        data = { 'name' : 'Computer & Thinking edited' },
        format = 'json'
    )
    assert response.status_code == HTTP_404_NOT_FOUND

  def test_get_success(self, adminClient,instructorId):
    response = adminClient.get(reverse('admin_instructor', args=(instructorId,)))
    resData = json.loads(response.content)
    assert response.status_code == HTTP_200_OK
    assert resData['id'] == instructorId


  def test_get_unauthorized(self, unauthClient,instructorId):
      response = unauthClient.get(reverse('admin_instructor', args=(instructorId,)))
      assert response.status_code == HTTP_401_UNAUTHORIZED

  def test_get_forbidden(self, client,instructorId):
      response = client.get(reverse('admin_instructor', args=(instructorId,)))
      assert response.status_code == HTTP_403_FORBIDDEN

  def test_get_notfound(self, adminClient):
    response = adminClient.get(reverse('admin_instructor', args=(999999,)))
    assert response.status_code == HTTP_404_NOT_FOUND

  def test_delete_success(self, adminClient,instructorId):
    response = adminClient.delete(reverse('admin_instructor', args=(instructorId,)))
    assert response.status_code == HTTP_200_OK
    assert User.objects.filter(id=instructorId).exists() == False

  def test_delete_unauthorized(self, unauthClient, instructorId):
      response = unauthClient.delete(reverse('admin_instructor', args=(instructorId,)))
      assert response.status_code == HTTP_401_UNAUTHORIZED

  def test_delete_forbidden(self, client, instructorId):
      response = client.delete(reverse('admin_instructor', args=(instructorId,)))
      assert response.status_code == HTTP_403_FORBIDDEN

  def test_delete_notfound(self, adminClient):
      response = adminClient.delete(reverse('admin_instructor', args=(999999,)))
      assert response.status_code == HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestAdminInstructorsAPI:
  def test_get_success(self,adminClient):
      response = adminClient.get(reverse('admin_instructors'))
      resData = json.loads(response.content)
      print(resData)
      assert response.status_code == HTTP_200_OK
      assert type(resData) == list

  def test_get_unauthorized(self,unauthClient):
      response = unauthClient.get(reverse('admin_instructors'))
      assert response.status_code == HTTP_401_UNAUTHORIZED

  def test_get_forbidden(self,client):
      response = client.get(reverse('admin_instructors'))
      assert response.status_code == HTTP_403_FORBIDDEN
  
  def test_post_success(self,adminClient,instructorValidData):
    print('Valid Data in the test : ',instructorValidData)
    response = adminClient.post(
      reverse('admin_instructors'),
      data = instructorValidData,
      format = 'json'
    )
    assert response.status_code == HTTP_201_CREATED

  def test_post_unauthorized(self, unauthClient):
    response = unauthClient.post(reverse('admin_instructors'),)
    assert response.status_code == HTTP_401_UNAUTHORIZED
    
  def test_post_badrequest(self, adminClient,invalidData):
    response = adminClient.post(
      reverse('admin_instructors'),
      data = invalidData,
      format = 'json'
    )
    assert response.status_code == HTTP_400_BAD_REQUEST

  
  def test_post_forbidden(self,client,invalidData):
    response = client.post(
      reverse('admin_instructors'),
      data = invalidData,
      format = 'json'
    )
    assert response.status_code == HTTP_403_FORBIDDEN