import pytest

from django.urls import reverse
from rest_framework.status import *
from fixtures import *
from courses.models import Topic


@pytest.mark.django_db
class TestAdminTopicAPI:
    def test_put_success(self, adminClient, topicId):
        response = adminClient.put(
            reverse('admin-topic', args=(topicId,)),
            data = { 'name' : 'Computer & Thinking edited' },
            format = 'json'
        )
        resData = json.loads(response.content)
        assert response.status_code == HTTP_200_OK
        assert Topic.objects.get(id=resData['id']).name == 'Computer & Thinking edited'

    def test_put_unauthorized(self, unauthClient, topicId):
        response = unauthClient.put(
            reverse('admin-topic', args=(topicId,)),
            data = { 'name' : 'Computer & Thinking edited' },
            format = 'json'
        )
        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_put_forbidden(self, client, topicId):
        response = client.put(
            reverse('admin-topic', args=(topicId,)),
            data = { 'name' : 'Computer & Thinking edited' },
            format = 'json'
        )
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_put_notfound(self, adminClient, topicId):
        response = adminClient.put(
            reverse('admin-topic', args=(999999,)),
            data = { 'name' : 'Computer & Thinking edited' },
            format = 'json'
        )
        assert response.status_code == HTTP_404_NOT_FOUND

    def test_get_success(self, adminClient, topicId):
        response = adminClient.get(reverse('admin-topic', args=(topicId,)))
        resData = json.loads(response.content)
        assert response.status_code == HTTP_200_OK
        assert resData['id'] == topicId

    def test_get_unauthorized(self, unauthClient, topicId):
        response = unauthClient.get(reverse('admin-topic', args=(topicId,)))
        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_get_forbidden(self, client, topicId):
        response = client.get(reverse('admin-topic', args=(topicId,)))
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_get_notfound(self, adminClient):
        response = adminClient.get(reverse('admin-topic', args=(999999,)))
        assert response.status_code == HTTP_404_NOT_FOUND

    def test_delete_success(self, adminClient, topicId):
        response = adminClient.delete(reverse('admin-topic', args=(topicId,)))
        assert response.status_code == HTTP_200_OK
        assert User.objects.filter(id=topicId).exists() == False

    def test_delete_unauthorized(self, unauthClient, topicId):
        response = unauthClient.delete(reverse('admin-topic', args=(topicId,)))
        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_delete_forbidden(self, client, topicId):
        response = client.delete(reverse('admin-topic', args=(topicId,)))
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_delete_notfound(self, adminClient):
        response = adminClient.delete(reverse('admin-topic', args=(999999,)))
        assert response.status_code == HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestAdminTopicsAPI:
    def test_get_success(self, adminClient):
        response = adminClient.get(reverse('admin-topics'))
        resData = json.loads(response.content)
        print(resData)
        assert response.status_code == HTTP_200_OK
        assert type(resData) == list

    def test_get_unathorized(self, unauthClient):
        response = unauthClient.get(reverse('admin-topics'))
        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_get_forbidden(self, client):
        response = client.get(reverse('admin-topics'))
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_post_success(self, adminClient):
        response = adminClient.post(
            reverse('admin-topics'),
            data = {'name' : 'Critical Thingking'},
            format = 'json'
        )
        resData = json.loads(response.content)
        assert response.status_code == HTTP_201_CREATED
        assert Topic.objects.filter(id = resData['id']).exists() == True

    def test_post_unauthorized(self, unauthClient):
        response = unauthClient.post(
            reverse('admin-topics'),
            data = {'name' : 'Critical Thingking'},
            format = 'json'
        )
        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_post_forbidden(self, client):
        response = client.post(
            reverse('admin-topics'),
            data = {'name' : 'Critical Thingking'},
            format = 'json'
        )
        assert response.status_code == HTTP_403_FORBIDDEN

