import pytest
import json

from django.urls import reverse

from rest_framework.status import *

from hosts.models import Host

from fixtures import *

@pytest.mark.django_db
class TestAdminHostAPI:
  def test_post_success(self,adminClient,hostValidData):
    response = adminClient.post(reverse('admin_hosts'),data=hostValidData,format='json')
    resData=json.loads(response.content)
    assert response.status_code == HTTP_201_CREATED
    assert Host.objects.filter(id=resData['id']).exists() == True

  def test_post_unauthorized(self,unauthClient,hostValidData):
    response = unauthClient.post(reverse('admin_hosts'),data=hostValidData,format='json')
    assert response.status_code==HTTP_401_UNAUTHORIZED
  
  def test_post_forbidden(self,client,hostValidData):
    response = client.post(reverse('admin_hosts'),data=hostValidData,format='json')
    assert response.status_code == HTTP_403_FORBIDDEN

  def test_post_badrequest(self,adminClient,hostInvalidData):
    response = adminClient.post(reverse('admin_hosts'),data=hostInvalidData,format='json')
    assert response.status_code==HTTP_400_BAD_REQUEST
  
  def test_get_success(self,adminClient):
    response = adminClient.get(reverse('admin_hosts'))
    resData = json.loads(response.content)
    assert response.status_code == HTTP_200_OK
    assert type(resData) == list
  
  def test_get_unauthorized(self,unauthClient):
    response = unauthClient.get(reverse('admin_hosts'))
    assert response.status_code == HTTP_401_UNAUTHORIZED

  def test_get_forbidden(self,client):
    response = client.get(reverse('admin_hosts'))
    assert response.status_code == HTTP_403_FORBIDDEN

@pytest.mark.django_db
class TestAdminHost:
  def test_put_success(self,adminClient,hostId):
    response = adminClient.put(
      reverse('admin_host',args=(hostId,)),
      data={
        'status':'Shortlisted'
      },
      format='json'
    )
    resData = json.loads(response.content)
    assert response.status_code == HTTP_200_OK
    assert resData.get('status') == 'Shortlisted'
  
  def test_put_unauthorized(self,unauthClient,hostId):
    response = unauthClient.put(
      reverse('admin_host',args=(hostId,)),
      data={
        'status':'Shortlisted'
      },
      format='json'
    )
    assert response.status_code == HTTP_401_UNAUTHORIZED
  
  def test_put_forbidden(self,client,hostId):
    response = client.put(
      reverse('admin_host',args=(hostId,)),
      data={
        'status':'Shortlisted'
      },
      format='json'
    )
    assert response.status_code == HTTP_403_FORBIDDEN

  def test_put_notfound(self,adminClient):
    response = adminClient.put(
      reverse('admin_host',args=(9999,)),
      data={
        'status':'Shortlisted'
      },
      format='json'
    )
    assert response.status_code == HTTP_404_NOT_FOUND

  def test_get_success(self,adminClient,hostId):
    response = adminClient.get(reverse('admin_host',args=(hostId,)))
    assert response.status_code == HTTP_200_OK 
  
  def test_get_unauthorized(self,unauthClient,hostId):
    response = unauthClient.get(reverse('admin_host',args=(hostId,)))
    assert response.status_code == HTTP_401_UNAUTHORIZED

  def test_get_forbidden(self,client,hostId):
    response = client.get(reverse('admin_host',args=(hostId,)))
    assert response.status_code == HTTP_403_FORBIDDEN
  
  def test_get_notfound(self,adminClient):
    response = adminClient.get(reverse('admin_host',args=(987,)))
    assert response.status_code == HTTP_404_NOT_FOUND

  def test_delete_sucess(self,adminClient,hostId):
    response = adminClient.delete(reverse('admin_host',args=(hostId,)))
    assert response.status_code == HTTP_200_OK
  
  def test_delete_unauthorized(self,unauthClient,hostId):
    response = unauthClient.delete(reverse('admin_host',args=(hostId,)))
    assert response.status_code == HTTP_401_UNAUTHORIZED
  
  def test_delete_forbidden(self,client,hostId):
    response = client.delete(reverse('admin_host',args=(hostId,)))
    assert response.status_code == HTTP_403_FORBIDDEN

@pytest.mark.django_db
class TestHost:
  def test_post_success(self,client,hostValidData):
    response=client.post(reverse('host'),data=hostValidData,format='json')
    assert response.status_code == HTTP_201_CREATED

  def test_post_unauthorized(self,unauthClient,hostValidData):
    response=unauthClient.post(reverse('host'),data=hostValidData,format='json')
    assert response.status_code == HTTP_401_UNAUTHORIZED
  
  def test_post_badrequest(self,client,hostInvalidData):
    response = client.post(reverse('host'),data=hostInvalidData,format='json')
    assert response.status_code==HTTP_400_BAD_REQUEST

  @pytest.mark.usefixtures('hostId')
  def test_put_success(self,client):
    response = client.put(
      reverse('host'),
      data={
        'hostingType':'Split'
      },
      format='json'
    )
    resData = json.loads(response.content)
    assert resData.get('hostingType') == 'Split'
  
  @pytest.mark.usefixtures('hostId')
  def test_put_unauthorized(self,unauthClient,hostValidData):
    response = unauthClient.put(
      reverse('host'),
      data={
        'hostingType':'Split'
      },
      format='json'
    )
    assert response.status_code == HTTP_401_UNAUTHORIZED
  
  @pytest.mark.usefixtures('hostId')
  def test_put_badrequest(self,client,hostInvalidData):
    response = client.put(reverse('host'),data=hostInvalidData,format='json')
    assert response.status_code == HTTP_400_BAD_REQUEST

  @pytest.mark.usefixtures('hostId')
  def test_get_success(self,client):
    response = client.get(reverse('host'),format='json')
    assert response.status_code == HTTP_200_OK
  
  @pytest.mark.usefixtures('hostId')
  def test_get_unauthorized(self,unauthClient):
    response = unauthClient.get(reverse('host'),format='json')
    assert response.status_code == HTTP_401_UNAUTHORIZED