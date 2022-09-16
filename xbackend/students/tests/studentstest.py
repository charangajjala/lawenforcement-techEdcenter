import pytest
import io

from django.urls import reverse
from django.core.files import File
from rest_framework.status import *
from fixtures import *

@pytest.mark.django_db
class TestStandardStudentsAPI:
  def test_post_success(self, client, studentValidData2):
        response = client.post(
            reverse('student'),
            data = studentValidData2,
            format = 'json'
        )

        assert response.status_code == HTTP_201_CREATED

  def test_post_unauthorized(self, unauthClient,studentValidData2):
        response = unauthClient.post(
            reverse('student'),
            data = studentValidData2,
            format = 'json'
        )
        assert response.status_code == HTTP_401_UNAUTHORIZED

  def test_put_success(self, client2):
      response = client2.put(
          reverse('student'),
          data = {
              'comments':'This is the newest agency'
              },
          format = 'json'
      )
      resData = json.loads(response.content)
      assert response.status_code == HTTP_200_OK

  def test_put_unauthorized(self, unauthClient):
      response = unauthClient.put(
          reverse('student'),
          data = {
              'comments':'This is the newest agency'
              },
          format = 'json'
      )
      assert response.status_code == HTTP_401_UNAUTHORIZED

  def test_put_notfound(self, client):
      response = client.put(
          reverse('student'),
          data = {
              'old':'This is the newest agency'
              },
          format = 'json'
      )
      assert response.status_code == HTTP_404_NOT_FOUND

  def test_get_success(self, client2 ):
      response = client2.get(reverse('student'))
      resData = json.loads(response.content)
      assert response.status_code == HTTP_200_OK

  def test_get_unauthorized(self, unauthClient):
      response = unauthClient.get(reverse('student'))
      assert response.status_code == HTTP_401_UNAUTHORIZED

  def test_get_notfound(self, client):
      response = client.get(reverse('student'))
      assert response.status_code == HTTP_404_NOT_FOUND
