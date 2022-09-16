import pytest
import io
import pathlib
import json

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.core.files import File

from users.models import *
from students.models import *

def getUser(email, admin=False, sudo=False):
    user = User.objects.create(
        firstName = 'john',
        lastName = 'snow',
        email = email,
        password = 'johnpassword',
        isAdmin = admin,
        isSuperUser = sudo
    )
    return user 

@pytest.fixture
def adminClient(db):
    user = getUser('john1@snow.com', True, False)
    resp = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION = 'Bearer {}'.format(resp.access_token))
    return client

@pytest.fixture
def sudoClient(db):
  user = getUser('john2@snow.com',True, False)
  resp = RefreshToken.for_user(user)
  client = APIClient()
  client.credentials(HTTP_AUTHORIZATION = 'Bearer {}'.format(resp.access_token))
  return client

@pytest.fixture
def unauthClient(db):
  return APIClient()

@pytest.fixture
def client(db):
  user = getUser('john2@snow.com')
  resp = RefreshToken.for_user(user)
  client = APIClient()
  client.credentials(HTTP_AUTHORIZATION = 'Bearer {}'.format(resp.access_token))
  return client

@pytest.fixture
def userId(db):
  u = getUser('john1@doe.com')
  return u.id

@pytest.fixture
def studentValidData(userId):
  data = {
    'userId':userId,
    'agencyName':'agency',
    'comments':'This is a new comment',
    'adminNotes':['item1','item2'],
    'isActive':'True'
  }
  return data

@pytest.fixture
def studentValidData2(userId):
  data = {
    'userId':userId,
    'agencyName':'agency',
    'comments':'This is a new comment',
  }
  return data

@pytest.fixture
def studentId(db):
  user=getUser('john2@doe.com')
  student = Student.objects.create(
    **dict(
      user = user,
      comments = 'This is a new comment',
      agencyName = 'agency',
      isActive = 'True',
    )
  )
  return student.id

@pytest.fixture
def client2(db):
  user=getUser('john3@doe.com')
  student = Student.objects.create(
    **dict(
      user= user,
      comments = 'This is a old comment',
      agencyName = 'oldagency',
    )
  )
  resp = RefreshToken.for_user(user)
  client = APIClient()
  client.credentials(HTTP_AUTHORIZATION = 'Bearer {}'.format(resp.access_token))
  return client

@pytest.fixture
def adminClient2(db):
    user = getUser('john1@snow.com', True, False)
    student = Student.objects.create(
      **dict(
        user= user,
        comments = 'This is a old comment',
        adminNotes = ['item1'],
        agencyName = 'oldagency',
      )
    )
    resp = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION = 'Bearer {}'.format(resp.access_token))
    return client


