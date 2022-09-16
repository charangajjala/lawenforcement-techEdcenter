import pytest
import io
import pathlib
import json

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import *
from instructors.models import *
from django.urls import reverse
from django.test import override_settings
import tempfile
from PIL import Image
from meta.models import File

#defining file data for session wide
def get_image(temp_file):
  image=Image.new("RGB",size=(300,300),color=(255,0,0))
  image.save(temp_file,'jpeg')
  return temp_file

@pytest.fixture(autouse=True)
@override_settings(MEDIA_ROOT=tempfile.gettempdir())
def image():
  temp_file = tempfile.NamedTemporaryFile()
  test_image = get_image(temp_file)
  #test_image.seek(0)
  file = File.objects.create(
    name= test_image.name,
    file = test_image.name,
  )
  return file

def getUser(email, admin=False, sudo=False):
    user = User.objects.create(
        title = 'title2',
        firstName = 'john',
        lastName = 'snow',
        email = email,
        password = 'johnpassword',
        isAdmin = admin,
        isSuperUser = sudo
    )
    return user

def getagencyAddress():
  agencyAddress = Address.objects.create(
    address1 = '1111 bond st',
    city='Irvnie',
    state = 'TX',
    zip = '51750'
  )
  return agencyAddress

def getagencyContact():
  agencyContact = Contact.objects.create(
    title = 'title',
    name = 'john',
    email = 'john3@gmail.com',
    phone = '912104554',
  )
  return agencyContact

def getemergencyContact():
  emergencyContact = Contact.objects.create(
    title = 'title',
    name = 'johnSnow',
    email = 'johnsnow@email.com',
    phone = '9988776655',
  )
  return emergencyContact

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
def client2(db):
  user = getUser('john2@snow.com')
  instructor = Instructor.objects.create(
    user = user,
    dob='2020-12-12',
    ssn='ssn',
    bio='bio',
    agencyName='old agenc',
    agencyAddress=getagencyAddress(),
    agencyContact = getagencyContact(),
    emergencyContact = getemergencyContact(),
    retiredDate = '2021-05-05',
    closestAirports = 'Dallas',
    preferredAirports = 'Dallas',
    travelNotes = 'Nothing'
  )
  resp = RefreshToken.for_user(user)
  client = APIClient()
  client.credentials(HTTP_AUTHORIZATION = 'Bearer {}'.format(resp.access_token))
  return client

@pytest.fixture
def applicant2(db):
  user = getUser('john2@snow.com',True, False)
  applicant = Applicant.objects.create(
    user =user,
    comments='Old Comment',
  )
  resp = RefreshToken.for_user(user)
  client = APIClient()
  client.credentials(HTTP_AUTHORIZATION = 'Bearer {}'.format(resp.access_token))
  return client

@pytest.fixture
def userId(db):
  u = getUser('john31@doe.com')
  return u.id

def getinstructor(obj):
  instructor = Instructor.objects.create(
    user = getUser('john32@doe.com'),
    image = obj,
    dob='2020-12-12',
    ssn='ssn',
    bio='bio',
    agencyName='old agenc',
    agencyAddress=getagencyAddress(),
    agencyContact = getagencyContact(),
    emergencyContact = getemergencyContact(),
    retiredDate = '2021-05-05',
    closestAirports = 'Dallas',
    preferredAirports = 'Dallas',
    travelNotes = 'Nothing'
  )
  return instructor

def getApplicant():
  applicant = Applicant.objects.create(
    user = getUser('john32@doe.com'),
    comments='This is a comment',
  )
  return applicant

@pytest.fixture
def applicantId(db):
  applicant = getApplicant()
  return applicant.id

@pytest.fixture
def instructorId(db,image):
  instructor = getinstructor(image)
  return instructor.id


@pytest.fixture
def instructorValidData(userId):
  data = {
    'userId':userId,
    'dob': '2020-12-02',
    'ssn': '223',
    'bio':'This is my bio',
    'agencyName':'SuryaAgency',
    'agencyAddress':{
      'address1':'reddy and reddy colony',
      'address2':'2nd street',
      'city':'tirupati',
      'state':'AP',
      'zip':'517501'
    },
    'agencyContact':{
      'title':'main',
      'name':'Surya',
      'email':"surya@gmail.com",
      'email2':'surya3@gmail.com',
      'phone':'9876543210',
      'phone2':'9876543215'   
    },
    'emergencyContact':{
      'title':'main2',
      'name':'Surya2',
      'email':'surya2@gmail.com',
      'email2':'surya4@gmail.com',
      'phone':'9876543121',
      'phone2':'9491257681'
    },
    'isActive':'True',
    'retiredDate':'2021-12-24',
    'closestAirports':'Garuda',
    'preferredAirports':'Garuda',
    'travelNotes':'Nothning Much'
  }
  return data

@pytest.fixture
def invalidData():
    return {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'johnecom',
        'password': 'strong password',
        'randomField': 'random data'
    }

@pytest.fixture
def applicantValidData(userId):
  data = {
    'userId':userId,
    'status':2,
    "comments": 'This is a comment'
  }
  return data

@pytest.fixture
def applicantValidData2():
  return {
        'title':'title3',
        'firstName': 'John',
        'lastName': 'Doe',
        'phone':'9876543210',
        'email': 'john1e21@doe.com',
        'password': 'strong password',
        'comments':'This is a comment'
    }

@pytest.fixture
def applicantInValidData():
  return {
        'firstNam': 'John',
        'lastName': 'Doe',
        'phone':'9876543210',
        'email': 'john1e21@doe.com',
        'password': 'strong password',
        'comments':'This is a comment',
    }

@pytest.fixture
def client3(db):
  client = APIClient()
  return client