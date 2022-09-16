import pytest
import io

from django.urls import reverse
from django.core.files import File
from rest_framework.status import *
from fixtures import *

@pytest.mark.django_db
class TestAdminStudentsAPI:

  def test_post_success(self, adminClient, studentValidData):
        response = adminClient.post(
            reverse('admin_students'),
            data = studentValidData,
            format = 'json'
        )

        assert response.status_code == HTTP_201_CREATED

  def test_post_unauthorized(self, unauthClient,studentValidData):
        response = unauthClient.post(
            reverse('admin_students'),
            data = studentValidData,
            format = 'json'
        )
        assert response.status_code == HTTP_401_UNAUTHORIZED
  
  def test_post_forbidden(self, client,studentValidData):
        response = client.post(
            reverse('admin_students'),
            data = studentValidData,
            format = 'json'
        )
        assert response.status_code == HTTP_403_FORBIDDEN

  def test_get_success(self, adminClient):
        response = adminClient.get(reverse('admin_students'))
        resData = json.loads(response.content)
        assert response.status_code == HTTP_200_OK
        assert type(resData) == list
        #assert len(resData) > 0

  def test_get_unauthorized(self, unauthClient):
      response = unauthClient.get(reverse('admin_students'))
      assert response.status_code == HTTP_401_UNAUTHORIZED

  def test_get_forbidden(self, client):
      response = client.get(reverse('admin_students'))
      assert response.status_code == HTTP_403_FORBIDDEN

@pytest.mark.django_db
class TestAdminStudentAPI:
  def test_get_success(self, adminClient, studentId):
      response = adminClient.get(reverse('admin_student', args=(studentId,)))
      resData = json.loads(response.content)
      assert response.status_code == HTTP_200_OK
      assert resData['id'] == studentId

  def test_get_unauthorized(self, unauthClient, studentId):
      response = unauthClient.get(reverse('admin_student', args=(studentId,)))
      assert response.status_code == HTTP_401_UNAUTHORIZED

  def test_get_forbidden(self, client, studentId):
      response = client.get(reverse('admin_student', args=(studentId,)))
      assert response.status_code == HTTP_403_FORBIDDEN

  def test_get_notfound(self, adminClient):
      response = adminClient.get(reverse('admin_student', args=(999999,)))
      assert response.status_code == HTTP_404_NOT_FOUND

  def test_delete_success(self, adminClient, studentId):
      response = adminClient.delete(reverse('admin_student', args=(studentId,)))
      assert response.status_code == HTTP_200_OK
      assert Student.objects.filter(id=studentId).exists() == False

  def test_delete_unauthorized(self, unauthClient, studentId):
      response = unauthClient.delete(reverse('admin_student', args=(studentId,)))
      assert response.status_code == HTTP_401_UNAUTHORIZED

  def test_delete_forbidden(self, client, studentId):
      response = client.delete(reverse('admin_student', args=(studentId,)))
      assert response.status_code == HTTP_403_FORBIDDEN

  def test_delete_notfound(self, adminClient):
      response = adminClient.delete(reverse('admin_student', args=(999999,)))
      assert response.status_code == HTTP_404_NOT_FOUND

  def test_put_success(self, adminClient, studentId):
      response = adminClient.put(
          reverse('admin_student', args=(studentId,)),
          data = {
              'comments':'This is the newest agency'
              },
          format = 'json'
      )
      resData = json.loads(response.content)
      assert response.status_code == HTTP_200_OK
      assert Student.objects.get(id=studentId).comments == 'This is the newest agency'

  def test_put_unauthorized(self, unauthClient, studentId):
      response = unauthClient.put(
          reverse('admin_student', args=(studentId,)),
          data = {
              'comments':'This is the newest agency'
              },
          format = 'json'
      )
      assert response.status_code == HTTP_401_UNAUTHORIZED

  def test_put_forbidden(self, client, studentId):
      response = client.put(
          reverse('admin_student', args=(studentId,)),
          data = {
              'comments':'This is the newest agency'
              },
          format = 'json'
      )
      assert response.status_code == HTTP_403_FORBIDDEN

  def test_put_notfound(self, adminClient):
      response = adminClient.put(
          reverse('admin_student', args=(999999,)),
          data = {
              'comments':'This is the newest agency'
              },
          format = 'json'
      )
      assert response.status_code == HTTP_404_NOT_FOUND