import pytest

from django.urls import reverse
from rest_framework.status import *
from fixtures import *

@pytest.mark.django_db
class TestTracksAPI:
    def test_getall_success(self, unauthClient):
        response = unauthClient.get(reverse('tracks'))
        assert response.status_code == HTTP_200_OK

    def test_get_success(self, unauthClient,trackId):
        response = unauthClient.get(reverse('track',args=(trackId,)),format='json')
        assert response.status_code == HTTP_200_OK

    def test_get_notfound(self, unauthClient):
        response = unauthClient.get(reverse('track',args=(12345,)),format='json')
        assert response.status_code == HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestAdminTracksAPI:
   
    def test_post_success(self, adminClient,trackValidData):

        response = adminClient.post(
            reverse('admin-tracks'),
            data = trackValidData,
            format='json'
        )
        
        assert response.status_code == HTTP_201_CREATED
    
    def test_post_unauthorized(self, unauthClient):
        #with open(self.file, 'rb') as fp:
        response = unauthClient.post(
            reverse('admin-tracks'),
            data = {'title':'Artificial techinal Intelligence','shortName':'ATI'},
        )

        assert response.status_code == HTTP_401_UNAUTHORIZED
    
    def test_post_badrequest(self, adminClient):
        response = adminClient.post(
            reverse('admin-tracks'),
            data = {'title':'Artificial techinal Intelligence','shortName':1},
        )
        assert response.status_code == HTTP_400_BAD_REQUEST
    
    def test_post_forbidden(self, client):
        with open(self.file, 'rb') as fp:
            response = client.post(
                reverse('admin-tracks'),
                data = {'title':'Artificial techinal Intelligence','shortName':'ATI','logo':fp},
            )
        assert response.status_code == HTTP_403_FORBIDDEN
    
    def test_get_success(self, adminClient):
        response = adminClient.get(reverse('admin-tracks'),)
        assert response.status_code == HTTP_200_OK

    def test_get_unauthorized(self, unauthClient):
        response = unauthClient.get(reverse('admin-tracks'),)
        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_get_forbidden(self, client):
        response = client.get(reverse('admin-tracks'),)
        assert response.status_code == HTTP_403_FORBIDDEN

@pytest.mark.django_db
class TestAdminTrackAPI:
   
    def test_put_success(self, adminClient):
        response = adminClient.put(self.url, data = {'title':'Artifici edited'})
        assert response.status_code == HTTP_200_OK
    
    def test_put_file_success(self, adminClient):
        with open(self.file1, 'rb') as fp:
            response = adminClient.put(self.url, data = {'logo': fp})

        assert response.status_code == HTTP_200_OK

    def test_put_badrequest(self, adminClient):
        response = adminClient.put(self.url, data = {'logo':'Artifici edited'})
        assert response.status_code == HTTP_400_BAD_REQUEST
    
    def test_put_notfound(self, adminClient):
        response = adminClient.put(self.url404, data = {'title':'Artifici edited'})
        assert response.status_code == HTTP_404_NOT_FOUND
        
    def test_put_unauthorized(self, unauthClient):
        response = unauthClient.put(self.url, data = {'title':'Artifici edited'})
        assert response.status_code == HTTP_401_UNAUTHORIZED
        
    def test_put_forbidden(self, client):
        response = client.put(self.url, data = {'title':'Artifici edited'})
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_get_success(self, adminClient):
        response = adminClient.get(self.url)
        assert response.status_code == HTTP_200_OK

    def test_get_notfound(self, adminClient):
        response = adminClient.get(self.url404)
        assert response.status_code == HTTP_404_NOT_FOUND
        
    def test_get_unauthorized(self, unauthClient):
        response = unauthClient.get(self.url)
        assert response.status_code == HTTP_401_UNAUTHORIZED
        
    def test_get_forbidden(self, client):
        response = client.get(self.url)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_delete_success(self, adminClient):
        response = adminClient.delete(self.url)
        assert response.status_code == HTTP_200_OK

    def test_delete_notfound(self, adminClient):
        response = adminClient.delete(self.url404)
        assert response.status_code == HTTP_404_NOT_FOUND
        
    def test_delete_forbidden(self, client):
        response = client.delete(self.url)
        assert response.status_code == HTTP_403_FORBIDDEN
        
    def test_delete_unauthorized(self, unauthClient):
        response = unauthClient.delete(self.url)
        assert response.status_code == HTTP_401_UNAUTHORIZED
