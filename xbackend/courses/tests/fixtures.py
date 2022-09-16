import pytest
import io
import pathlib
import json
import tempfile

from PIL import Image

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.core.files import File
from django.test import override_settings

from users.models import User
from courses.models import CertificationTrack
from courses.models import Topic, Course, Agenda
from meta.models import File

#user for admin sudo and client
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

#users defined from getUser function
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

#temporay file for file upload
@pytest.fixture(scope='function',autouse=True)
@override_settings(MEDIA_ROOT=tempfile.gettempdir())
def file():
    temp_file = tempfile.NamedTemporaryFile()
    temp_file.write(b'This is the content of the file')
    temp_file.seek(0)
    file = File.objects.create(
        name = temp_file.name,
        file = temp_file.name
    )
    return file.id

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
  file = File.objects.create(
    name= test_image.name,
    file = test_image.name,
  )
  return file.id

@pytest.fixture(autouse=True)
@override_settings(MEDIA_ROOT=tempfile.gettempdir())
def imageFile():
  temp_file = tempfile.NamedTemporaryFile()
  test_image = get_image(temp_file)
  return test_image

@pytest.fixture(scope='function',autouse=True)
def courseId(db):
    courseObj = Course.objects.create(
    courseNum="PE0111",
    title = 'Awsome title',
    subTitle='some sample suntitle',
    shortDesc='sample short desc',
    description = [
        "test description 1",
        "test description 2"
    ],
    targetAudience = 'sample who can attend',
    prerequisites = 'sample pre requisites',
    days = 2
    )
    courseObj.agenda.add(Agenda.objects.create(day=1, value=["test agenda", "test agenda1"]))
    courseObj.agenda.add(Agenda.objects.create(day=2, value=["test agenda", "test agenda1"]))
    return courseObj.id

@pytest.fixture(scope='function',autouse=True)
def topicId(db):
    topicObj=Topic.objects.create(
        name='Topic 1'
    )
    return topicObj.id

@pytest.fixture(scope='function')
def trackId(db,image,courseId):
    fileObj = File.objects.get(id=image)
    courseObj = Course.objects.get(id=courseId)
    trackObj = CertificationTrack.objects.create(
        title='Track 1',
        shortName='T1',
        logo=fileObj,
        numCourses=3,
        what='Nothing to describe',
        why='Nothing to say',
        how='Nothing to do',
        maintainance='Nothing to maintain',
        who=['Its me'],
        benefits=['No benefits'],
        requirements=['Nothing required especially'],
    )
    trackObj.requiredCourses.add(courseObj)
    return trackObj.id

#data
@pytest.fixture
def trackValidData(db,image):
    fileObj = File.objects.get(id=image)
    data = {
            'title': 'Artkjsvd',
            'shortName': 'ACA',
            'what': 'asdsvefasd',
            'why': 'asfdsfvde',
            'who': ['agrefvc','ljasgbfh;iu'],
            'benefits':['aafaevf','skjerthbgn'],
            'how': 'asfdsfefds',
            'requirements': ['qwfesdvxcz',';idrlgbu'],
            'maintainance': 'afwedsx',
            'numCourses': 5,
            'isActive':True,
            'logo': fileObj
        }
    return data

@pytest.fixture
def courseValidData():
    data = {
        "courseNum" : "AP1SDR",
        "title": "Awesome Title",
        "subTitle": "some sample subtitle",
        "shortDesc": "sample short description",
        "description": [
            "test description 1",
            "test description 2"
        ],
        "targetAudience": "sample who can attend",
        "prerequisites": "sample prerequisites",
        "days" : 2,
        "agenda": [
            {
                "value": [
                    "test agenda day1 1",
                    "test agenda day1 2"
                ],
                "day": 1
            },
            {
                "value": [
                    "test agenda day2 1",
                    "test agenda day2 2"
                ],
                "day": 2
            }
        ],
    }
    return data

@pytest.fixture
def courseInvalidData():
    data = {
        "title": "Awesome Title",
        "subTitle": "some sample subtitle",
        "shortDesc": "sample short description",
        "description": [
            "test description 1",
            "test description 2"
        ],
        "targetAudience": "sample who can attend",
        "prerequisites": "sample prerequisites",
        "days" : 2,
        "agenda": [
            {
                "value": [
                    "test agenda day1 1",
                    "test agenda day1 2"
                ],
                "day": 1
            },
            {
                "value": [
                    "test agenda day2 1",
                    "test agenda day2 2"
                ],
                "day": 2
            }
        ],
    }
    return data

@pytest.fixture
def trackInvalidData(db,image):
    fileObj = File.objects.get(id=image)
    data = {
            'shortName': 'ACA',
            'what': 'asdsvefasd',
            'why': 'asfdsfvde',
            'who': ['agrefvc','ljasgbfh;iu'],
            'benefits':['aafaevf','skjerthbgn'],
            'how': 'asfdsfefds',
            'requirements': ['qwfesdvxcz',';idrlgbu'],
            'maintainance': 'afwedsx',
            'numCourses': 5,
            'isActive':True,
            'logo': fileObj
        }
    return data
