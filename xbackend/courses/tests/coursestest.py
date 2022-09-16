import pytest
import io

from django.urls import reverse
from django.core.files import File
from rest_framework.status import *
from fixtures import *

@pytest.mark.django_db
class TestMaterialAPI:
    def test_post_success(self, adminClient,imageFile):
        response = adminClient.post(reverse('file-upload'),{'file':imageFile})
        assert response.status_code == HTTP_201_CREATED
 
    # def test_delete_success(self,adminClient,image):
    #     file=File.objects.get(id=image)
    #     print('THis is the file',type(file),getattr(file,'id'))
    #     response = adminClient.delete(reverse('file-upload'),{'file':file})
    #    assert response.status_code == HTTP_200_OK
 
    def test_post_unauthorized(self,unauthClient,imageFile):
        response = unauthClient.post(reverse('file-upload'),{'file':imageFile})
        assert response.status_code == HTTP_401_UNAUTHORIZED    

    def test_post_forbidden(self,client,imageFile):
        response = client.post(reverse('file-upload'),{'file':imageFile})
        assert response.status_code == HTTP_403_FORBIDDEN
    
    def test_post_badrequest(self,adminClient):
        response = adminClient.post(reverse('file-upload'),{'file':256})
        assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR

    # def test_delete_unauthorized(self):
    #     pass
 
    # def test_delete_badrequest(self):
    #     pass

@pytest.mark.django_db
class TestCoursesAPI:
    def test_getall_success_authenticated(self, client):
        response = client.get(reverse('courses'),format='json')
        resData = json.loads(response.content)
        assert response.status_code == HTTP_200_OK
        assert type(resData) == list
    
    def test_getall_success_unauthenticated(self, unauthClient):
        response = unauthClient.get(reverse('courses'),format='json')
        resData = json.loads(response.content)
        assert response.status_code == HTTP_200_OK
        assert type(resData) == list

    def test_get_success_authenticated(self, client,courseId):
        response = client.get(reverse('course',args=(courseId,)),format='json')
        assert response.status_code == HTTP_200_OK

    def test_get_success_unauthenticated(self, unauthClient,courseId):
        response = unauthClient.get(reverse('course',args=(courseId,)),format='json')
        assert response.status_code == HTTP_200_OK

    def test_get_notfound(self, client):
        response = client.get(reverse('course',args=(256,)),format='json')
        assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestAdminCoursesAPI:
    def test_getall_success(self,adminClient):
        response = adminClient.get(reverse('admin-courses'),formt='json')
        resData = json.loads(response.content)
        assert response.status_code == HTTP_200_OK
        assert type(resData) == list

    def test_getall_unauthorized(self,unauthClient):
        response = unauthClient.get(reverse('admin-courses'),format='json')
        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_getall_forbidden(self,client):
        response = client.get(reverse('admin-courses'),format='json')
        assert response.status_code ==  HTTP_403_FORBIDDEN

    def test_post_success(self, adminClient, courseValidData):
        response = adminClient.post(
            reverse('admin-courses'),
            data = courseValidData,
            format = 'json'
        )
        resData = json.loads(response.content)
        assert response.status_code == HTTP_201_CREATED
        assert Course.objects.filter(id=resData['id']).exists() == True
    
    def test_post_unauthorized(self, unauthClient, courseValidData):
        response = unauthClient.post(
            reverse('admin-courses'),
            data = courseValidData,
            format = 'json'
        )

        assert response.status_code == HTTP_401_UNAUTHORIZED
    
    def test_post_badrequest(self, adminClient, courseInvalidData):
        response = adminClient.post(
            reverse('admin-courses'),
            data = courseInvalidData,
            format = 'json'
        )

        assert response.status_code == HTTP_400_BAD_REQUEST
    
    def test_post_forbidden(self, client, courseValidData):
        response = client.post(
            reverse('admin-courses'),
            data=courseValidData,
            format='json'
        )
        assert response.status_code == HTTP_403_FORBIDDEN

@pytest.mark.django_db
class TestAdminCourseAPI:
   
    def test_put_success(self, adminClient, courseId):
        response = adminClient.put(
            reverse('admin-course', args=(courseId,)),
            data = {
                "agenda": [
                    {
                        "day": 2,
                        "value": [
                            "updated agenda",
                            "updated agenda1"
                        ]
                    }
                ]
            },
            format = 'json'
        )
        assert response.status_code == HTTP_200_OK

    def test_put_badrequest(self, adminClient,courseId):
        response = adminClient.put(
            reverse('admin-course', args=(courseId,)),
            data = {
                'days':'the days'
            },
            format = 'json'
        )
        assert response.status_code == HTTP_400_BAD_REQUEST
    
    def test_put_notfound(self, adminClient):
        response = adminClient.put(
            reverse('admin-course', args=(1235,)),
            data = {
                "agenda": [
                    {
                        "day": 2,
                        "value": [
                            "updated agenda",
                            "updated agenda1"
                        ]
                    }
                ]
            },
            format = 'json'
        )
        assert response.status_code == HTTP_404_NOT_FOUND
        
    def test_put_unauthorized(self, unauthClient):
        pass
        
    def test_put_forbidden(self, client, courseId):
        response = client.put(
            reverse('admin-course', args=(courseId,)),
            data = {
                'days':'the days'
            },
            format = 'json'
        )
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_get_success(self, adminClient, courseId):
        response = adminClient.get(reverse('admin-course',args=(courseId,)),format='json')
        assert response.status_code == HTTP_200_OK

    def test_get_notfound(self, adminClient):
        response = adminClient.get(reverse('admin-course',args=(1234,)),format='json')
        assert response.status_code == HTTP_404_NOT_FOUND
        
    def test_get_unauthorized(self, unauthClient, courseId):
        response = unauthClient.get(reverse('admin-course',args=(courseId,)),format='json')
        assert response.status_code == HTTP_401_UNAUTHORIZED
        
    def test_get_forbidden(self, client, courseId):
        response = client.get(reverse('admin-course',args=(courseId,)),format='json')
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_delete_success(self, adminClient, courseId):
        response = adminClient.delete(reverse('admin-course',args=(courseId,)),format='json')
        assert response.status_code == HTTP_200_OK

    def test_delete_notfound(self, adminClient):
        response = adminClient.delete(reverse('admin-course',args=(12345,)),format='json')
        assert response.status_code == HTTP_404_NOT_FOUND
        
    def test_delete_forbidden(self, client, courseId):
        response = client.delete(reverse('admin-course',args=(courseId,)),format='json')
        assert response.status_code == HTTP_403_FORBIDDEN      
        
    def test_delete_unauthorized(self, unauthClient, courseId):
        response = unauthClient.delete(reverse('admin-course',args=(courseId,)),format='json')
        assert response.status_code == HTTP_401_UNAUTHORIZED
