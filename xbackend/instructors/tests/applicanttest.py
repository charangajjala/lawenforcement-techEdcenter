from instructors.models import *
from fixtures import *
import pytest
import json
import io

from django.urls import reverse
from django.core.files import File
from rest_framework.status import *


@pytest.mark.django_db
class TestAdminInstructorApplicantAPI:
  def test_get_success(self, adminClient,applicantId):
    response = adminClient.get(reverse('instructor_applicant', args=(applicantId,)))
    resData = json.loads(response.content)
    assert response.status_code == HTTP_200_OK
    assert resData['id'] == applicantId

  def test_get_unauthorized(self, unauthClient,applicantId):
      response = unauthClient.get(reverse('instructor_applicant', args=(applicantId,)))
      assert response.status_code == HTTP_401_UNAUTHORIZED

  def test_get_forbidden(self, client,applicantId):
      response = client.get(reverse('instructor_applicant', args=(applicantId,)))
      assert response.status_code == HTTP_403_FORBIDDEN

  def test_get_notfound(self, adminClient):
    response = adminClient.get(reverse('instructor_applicant', args=(999999,)))
    assert response.status_code == HTTP_404_NOT_FOUND

  def test_delete_success(self, applicant2,applicantId):
    response = applicant2.delete(reverse('instructor_applicant', args=(applicantId,)))
    assert response.status_code == HTTP_200_OK
    assert Applicant.objects.filter(id=applicantId).exists() == False

  def test_delete_unauthorized(self, unauthClient, applicantId):
      response = unauthClient.delete(reverse('instructor_applicant', args=(applicantId,)))
      assert response.status_code == HTTP_401_UNAUTHORIZED

  def test_delete_forbidden(self, client, applicantId):
      response = client.delete(reverse('instructor_applicant', args=(applicantId,)))
      assert response.status_code == HTTP_403_FORBIDDEN

  def test_delete_notfound(self, adminClient):
      response = adminClient.delete(reverse('instructor_applicant', args=(999999,)))
      assert response.status_code == HTTP_404_NOT_FOUND

  def test_put_success(self,applicant2,applicantId):
    response = applicant2.put(
        reverse('instructor_applicant', args=(applicantId,)),
        data = { 'comments' : 'New Comment' },
        format = 'json'
    )
    resData = json.loads(response.content)
    assert response.status_code == HTTP_200_OK
    assert Applicant.objects.get(id=applicantId).comments == 'New Comment'

  def test_put_unauthorized(self, unauthClient,applicantId):
    response = unauthClient.put(
        reverse('instructor_applicant', args=(applicantId,)),
        data = { 'comments' : 'New Comment' },
        format = 'json'
    )
    assert response.status_code == HTTP_401_UNAUTHORIZED

  def test_put_forbidden(self, client,applicantId):
    response = client.put(
        reverse('instructor_applicant', args=(applicantId,)),
        data = { 'comments' : 'New Comment' },
        format = 'json'
    )
    assert response.status_code == HTTP_403_FORBIDDEN


  def test_put_notfound(self, adminClient):
    response = adminClient.put(
        reverse('instructor_applicant', args=(999999,)),
        data = { 'name' : 'Computer & Thinking edited' },
        format = 'json'
    )
    assert response.status_code == HTTP_404_NOT_FOUND

  
@pytest.mark.django_db
class TestAdminInstructorApplicantsAPI:
  def test_get_success(self,adminClient):
      response = adminClient.get(reverse('instructor_applicants'))
      resData = json.loads(response.content)
      print(resData)
      assert response.status_code == HTTP_200_OK
      assert type(resData) == list

  def test_get_unauthorized(self,unauthClient):
      response = unauthClient.get(reverse('instructor_applicants'))
      assert response.status_code == HTTP_401_UNAUTHORIZED

  def test_get_forbidden(self,client):
      response = client.get(reverse('instructor_applicants'))
      assert response.status_code == HTTP_403_FORBIDDEN

@pytest.mark.django_db
class TestApplicantAPI:
  def test_post_success(self,client3,applicantValidData2):
    print('Valid Data in the test : ',applicantValidData2)
    response = client3.post(
      reverse('applicant'),
      data = applicantValidData2,
      format = 'json'
    )
    assert response.status_code == HTTP_201_CREATED

  def test_post_forbidden(self,client3,applicantInValidData):
    response = client3.post(
      reverse('applicant'),
      data = applicantInValidData,
      format = 'json'
    )
    assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR

  def test_get_success(self, applicant2):
      response = applicant2.get(reverse('applicant'))
      resData = json.loads(response.content)
      print(resData)
      assert response.status_code == HTTP_200_OK
