import pytest
import json

from django.urls import reverse
from rest_framework.status import *
from fixtures import *

@pytest.mark.django_db
class TestUserAPI:
    def test_put_success(self, adminClient, userId):
        response = adminClient.put(
            reverse('user', args=(userId,)),
            data = {
                'firstName': 'firstname edited',
                'password': 'Mp1!asap',
                'address': {
                    'zip':'51750',
                    'address2': '1918 Kuhl Avenue'
                }
            },
            format = 'json'
        )
        resData = json.loads(response.content)
        print('This is resdata',resData)
        assert response.status_code == HTTP_200_OK
        assert User.objects.get(id=userId).firstName == 'firstname edited'
        assert User.objects.get(id=userId).address.address2 == '1918 Kuhl Avenue'
    
    def test_put_success2(self, adminClient, userId):
        response = adminClient.put(
            reverse('user', args=(userId,)),
            data = {
                'firstName': 'firstname edited',
                'password': 'Mp1!asap',
            },
            format = 'json'
        )
        resData = json.loads(response.content)
        assert response.status_code == HTTP_200_OK
        assert User.objects.get(id=userId).firstName == 'firstname edited'

    def test_put_success3(self, adminClient, userId):
        response = adminClient.put(
            reverse('user', args=(userId,)),
            data = {
                'address': {
                    'address2': 'apt144',
                    'zip':'51750'
                }
            },
            format = 'json'
        )
        resData = json.loads(response.content)
        assert response.status_code == HTTP_200_OK
        assert User.objects.get(id=userId).address.address2 == 'apt144'
    
    def test_put_unauthorized(self, unauthClient, userId):
        response = unauthClient.put(
            reverse('user', args=(userId,)),
            data = {
                'firstName': 'firstname edited',
                'password': 'edited pass'
            },
            format = 'json'
        )
        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_put_forbidden(self, client, userId):
        response = client.put(
            reverse('user', args=(userId,)),
            data = {
                'firstName': 'firstname edited',
                'password': 'edited pass'
            },
            format = 'json'
        )
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_put_notfound(self, adminClient, userId):
        response = adminClient.put(
            reverse('user', args=(999999,)),
            data = {
                'firstName': 'firstname edited',
                'password': 'Mp1!asap'
            },
            format = 'json'
        )
        assert response.status_code == HTTP_404_NOT_FOUND

    def test_get_success(self, adminClient, userId):
        response = adminClient.get(reverse('user', args=(userId,)))
        resData = json.loads(response.content)
        assert response.status_code == HTTP_200_OK
        assert resData['id'] == userId

    def test_get_unauthorized(self, unauthClient, userId):
        response = unauthClient.get(reverse('user', args=(userId,)))
        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_get_forbidden(self, client, userId):
        response = client.get(reverse('user', args=(userId,)))
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_get_notfound(self, adminClient):
        response = adminClient.get(reverse('user', args=(999999,)))
        assert response.status_code == HTTP_404_NOT_FOUND

    def test_delete_success(self, adminClient, userId):
        response = adminClient.delete(reverse('user', args=(userId,)))
        assert response.status_code == HTTP_200_OK
        assert User.objects.filter(id=userId).exists() == False

    def test_delete_unauthorized(self, unauthClient, userId):
        response = unauthClient.delete(reverse('user', args=(userId,)))
        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_delete_forbidden(self, client, userId):
        response = client.delete(reverse('user', args=(userId,)))
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_delete_notfound(self, adminClient):
        response = adminClient.delete(reverse('user', args=(999999,)))
        assert response.status_code == HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestUsersAPI:
    def test_get_success(self, adminClient):
        response = adminClient.get(reverse('users'))
        resData = json.loads(response.content)
        print(resData)
        assert response.status_code == HTTP_200_OK
        assert type(resData) == list
        assert len(resData) > 0
#        assert ('name' in resData[0]) == True

    def test_get_unauthorized(self, unauthClient):
        response = unauthClient.get(reverse('users'))
        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_get_forbidden(self, client):
        response = client.get(reverse('users'))
        assert response.status_code == HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("data", [
        "validData1",
        "validData2",
        "validData3",
        "validData4",
        "validData5",
        "validData6"
    ])
    def test_post_success(self, adminClient, data, request):
        response = adminClient.post(
            reverse('users'),
            data = request.getfixturevalue(data),
            format = 'json'
        )
        print('This is response',response)
        resData = json.loads(response.content)
        print('This is resdata',resData)
        assert response.status_code == HTTP_201_CREATED
        assert User.objects.filter(id=resData['id']).exists() == True

    @pytest.mark.parametrize("data", [
        "validData1",
        "validData2",
        "validData3",
        "validData4",
        "validData5",
        "validData6"
    ])
    def test_post_unauthorized(self, unauthClient, data, request):
        response = unauthClient.post(
            reverse('users'),
            data = request.getfixturevalue(data),
            format = 'json'
        )
        assert response.status_code == HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize("data", [
        "validData1",
        "validData2",
        "validData3",
        "validData4",
        "validData5",
        "validData6"
    ])
    def test_post_forbidden(self, client, data, request):
        response = client.post(
            reverse('users'),
            data = request.getfixturevalue(data),
            format = 'json'
        )
        assert response.status_code == HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("data", [
        "invalidData1",
        "invalidData2",
        "invalidData3",
        "invalidData4",
        "invalidData5",
        "invalidData6"
    ])
    def test_post_badrequest(self, adminClient, data, request):
        response = adminClient.post(
            reverse('users'),
            data = request.getfixturevalue(data),
            format = 'json'
        )
        assert response.status_code == HTTP_400_BAD_REQUEST
