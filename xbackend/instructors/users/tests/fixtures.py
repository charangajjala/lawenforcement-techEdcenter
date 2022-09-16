import pytest
import io
import pathlib
import json

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.core.files import File

from users.models import User

def getUser(email, admin=False, sudo=False):
    user = User.objects.create(
        #title = 'title',
        firstName = 'john',
        lastName = 'snow',
        email = email,
        password = 'johnpassword',
        isAdmin = admin,
        isSuperUser = sudo
    )
    return user

@pytest.fixture
def sudoClient(db):
    user = getUser('john@snow.com', True, True)
    resp = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION = 'Bearer {}'.format(resp.access_token))
    return client

@pytest.fixture
def adminClient(db):
    user = getUser('john1@snow.com', True, False)
    resp = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION = 'Bearer {}'.format(resp.access_token))
    return client

@pytest.fixture
def client(db):
    user = getUser('john2@snow.com')
    resp = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION = 'Bearer {}'.format(resp.access_token))
    return client

@pytest.fixture
def unauthClient():
    return APIClient()

@pytest.fixture
def userId(db):
    u = getUser('john31@doe.com')
    return u.id

@pytest.fixture
def validData1():
    return {
        'title':'title',
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'johne@doe.com',
        'password': 'strong password',
        'phone': '1231231231',
        'isAdmin': True,
        'isSuperUser': False,
        'address': {
            'address1': '1111 bond st',
            'address2':'1112 bond st',
            'city': 'Irvnie',
            'state': 'TX',
            'zip': '75038'
        }
    }

@pytest.fixture
def validData2():
    return {
        'title':'title',
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'john1e@doe.com',
        'password': 'strong password'
    }

@pytest.fixture
def validData3():
    return {
        'title':'title',
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'johne@doe.com',
        'password': 'strong password',
        'phone': '1231231231'
    }

@pytest.fixture
def validData4():
    return {
        'title':'title',
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'johne@doe.com',
        'password': 'strong password',
        'isAdmin': False
    }

@pytest.fixture
def validData5():
    return {
        'title':'title',
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'johne@doe.com',
        'password': 'strong password',
        'isSuperUser': False
    }

@pytest.fixture
def validData6():
    return {
        'title':'title',
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'johne@doe.com',
    }

@pytest.fixture
def invalidData1():
    return {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'johnecom',
        'password': 'strong password'
    }

@pytest.fixture
def invalidData2():
    return {
        'firstName': 'John',
        'lastName': 'Doe',
        'password': 'strong password'
    }

@pytest.fixture
def invalidData3():
    return {
        'firstName': 'John',
        'email': 'johne@doe.com',
        'password': 'strong password'
    }

@pytest.fixture
def invalidData4():
    return {
        'lastName': 'Doe',
        'email': 'johne@doe.com',
        'password': 'strong password'
    }

@pytest.fixture
def invalidData5():
    return {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'johnecom',
        'password': 'strong password',
        'randomField': 'random data'
    }

@pytest.fixture
def invalidData6():
    return {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'johnecom',
        'password': 'strong password',
        'address': {
            'address1': 'my random address',
            'city': 'irving'
        }
    }
