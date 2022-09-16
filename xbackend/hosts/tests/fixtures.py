from enum import auto
import pytest, json,tempfile

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from hosts.models import Host,Location
from users.models import User
from meta.models import *

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

#user for admin sudo and client
def getUser(email,admin=False,sudo=False):
  userObj = User.objects.create(
    firstName = 'john',
    lastName = 'snow',
    email = email,
    password = 'Mp1!asap',
    isAdmin = admin,
    isSuperUser = sudo
  )
  return userObj

#users derived from getUser function
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
def adminClient(db):
    user = getUser('john2@snow.com', True, False)
    resp = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION = 'Bearer {}'.format(resp.access_token))
    return client  

@pytest.fixture
def client(db):
  print('Client page',User.objects.all())
  user = getUser('john2@snow.com') if len(User.objects.all()) == 0 else User.objects.all()[0]
  resp = RefreshToken.for_user(user)
  client = APIClient()
  client.credentials(HTTP_AUTHORIZATION = 'Bearer {}'.format(resp.access_token))
  return client

#file field
@pytest.fixture(scope='function',autouse=True)
@override_settings(MEDIA_ROOT=tempfile.gettempdir())
def file():
  temp_file = tempfile.NamedTemporaryFile()
  temp_file.write(b'Contents')
  temp_file.seek(0)
  file = File.objects.create(
    name= temp_file.name,
    file = temp_file.name,
  )
  return file.id


#user obj
@pytest.fixture(scope="function",autouse=True)
def user(db):
  userObj = User.objects.create(
    firstName = 'john',
    lastName = 'snow',
    email = "john@snow.com",
    password = 'Mp1!asap',
    isAdmin = False,
    isSuperUser = False
  ) 
  return userObj.id

#contact and address fixtures
@pytest.fixture(scope="function",autouse=True)
def address(db):
  addressObj = Address.objects.create(
    address1 = '1111 bond st',
    city='Irvnie',
    state = 'TX',
    zip = '51750'
  )
  return addressObj

# @pytest.fixture(name="address",scope='session',autouse=True)
# def address_fixture(django_db_blocker):
#   with django_db_blocker.unblock():
#     return address()

@pytest.fixture(scope="function",autouse=True)
def contact(db):
  contactObj = Contact.objects.create(
    title = 'title',
    name = 'john',
    email = 'john3@gmail.com',
    phone = '912104554',
  )
  return contactObj

# @pytest.fixture(name="contact",scope='session',autouse=True)
# def contact_fixture(django_db_blocker):
#   with django_db_blocker.unblock():
#     return contact()

#defining hostId
@pytest.fixture(scope='function')
def hostId(db,user,address,contact,file):
  userObj=User.objects.get(id=user)
  fileObj=File.objects.get(id=file)
  host=Host.objects.create(
    name='Host',
    website='http://google.com',
    contactUser=userObj,
    address=address,
    logo=fileObj,
    supervisorContact=contact,
    hostingType=1,
    status=2,
    comments='No comments',
  )
  return host.id

#host Data
@pytest.fixture
def hostValidData(user,file):
  data ={
    'name':'Host2',
    'website':'http://google.com',
    'contactUser':user,
    'address':{
        'address1': '1111 bond st',
        'city': 'Irvnie',
        'state': 'TX',
        'zip': '75038'
    },
    'logo':file,
    'supervisorContact':{
      'title':'title',
      'name' : 'john',
      'email' : 'john3@gmail.com',
      'phone' : '912104554',
    },
    'hostingType':'Speaker',
    'status':'Deferred',
    'comments':'No comments'
  }
  return data

@pytest.fixture
def hostInvalidData(user):
  data ={
    'name':'Host2',
    'website':'http://google.com',
    'contactUserId':user,
    'address':{
        'address1': '1111 bond st',
        'city': 'Irvnie',
        'state': 'TX',
        'zip': '75038'
    },
    'supervisorContact':{
      'title':'title',
      'name' : 54,
      'email' : 'john3@gmail.com',
      'phone' : '912104554',
    },
    'hostingType':3,
    'status':'Deferred',
    'comments':'No comments'
  }
  return data

#location fixtures
@pytest.fixture(scope='function')
def locationId(db,address,contact):
  location=Location.objects.create(
    name='Location',
    address=address,
    seats=112,
    locationContact=contact,
    notes='Note this down',
    closestAirports='garuda',
  )
  return location.id

#location data
@pytest.fixture
def locationValidData():
  data = {
    'name':'Location1',
    'address':{
      'address1': '1111 bond st',
      'city': 'Irvnie',
      'state': 'TX',
      'zip': '75038'
    },
    'seats':125,
    'notes':'Note this down',
    'locationContact':{
      'title':'title',
      'name' : 54,
      'email' : 'john3@gmail.com',
      'phone' : '912104554',
    },
    'closestAirports':'Garuda'
  }
  return data

@pytest.fixture
def locationInvalidData():
  data = {
    'name':'location1',
    'address':{
      'address1': '1111 bond st',
      'city': 'Irvnie',
      'state': 'TX',
      'zip': '75038'
    },
    'seats':'seats',
    'notes':'Note this down',
    'locationContact':{
      'title':'title',
      'name' : 54,
      'email' : 'john3@gmail.com',
      'phone' : '912104554',
    },
    'closestAirports':'Garuda'
  }
  return data