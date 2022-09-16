import io,pathlib,json,pytest

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from django.test import override_settings

from PIL import Image
import tempfile

from users.models import User
from instructors.models import Instructor
from meta.models import *
from hosts.models import Host,Location
from courses.models import Course,Agenda
from classes.models import Class
from students.models import Student

# from users.tests.fixtures import getUser
# from users.tests.fixtures import unauthClient,client,sudoClient,adminClient

from instructors.tests.fixtures import getagencyAddress,getagencyContact,getemergencyContact

# from courses.tests.fixtures import courseValidData,cId
# from instructors.tests.fixtures import instructorValidData

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
  user = getUser('john2@snow.com')
  resp = RefreshToken.for_user(user)
  client = APIClient()
  client.credentials(HTTP_AUTHORIZATION = 'Bearer {}'.format(resp.access_token))
  return client

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

#defining userId instructorId
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

@pytest.fixture(scope="function",autouse=True)
def instructor(db,image,address,contact):
  instructor = Instructor.objects.create(
    user = getUser('john1@snow.com'),
    image = image,
    dob='2020-12-12',
    ssn='ssn',
    bio='bio',
    agencyName='old agenc',
    agencyAddress=address,
    agencyContact = contact,
    emergencyContact = contact,
    retiredDate = '2021-05-05',
    closestAirports = 'Dallas',
    preferredAirports = 'Dallas',
    travelNotes = 'Nothing'
  )
  print('Instructor object genarated')
  return instructor.id

@pytest.fixture(scope="function",autouse=True)
def course(db):
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
  print('course Object generated')
  courseObj.agenda.add(Agenda.objects.create(day=1, value=["test agenda", "test agenda1"]))
  courseObj.agenda.add(Agenda.objects.create(day=2, value=["test agenda", "test agenda1"]))
  return courseObj.id

@pytest.fixture(scope="function",autouse=True)
def location(db,address,contact):
  location = Location.objects.create(
    name='location1',
    address=address,
    seats=150,
    isWifiEnabled=True,
    closestAirports='Garuda',
    locationContact=contact,
    notes='There is nothing to note in here',
  )
  print('location Object genarated')
  return location.id

@pytest.fixture(scope="function",autouse=True)
def host(db,address,image,user,contact):
  userObj = User.objects.get(id=user)
  host = Host.objects.create(
    name='Host',
    address = address,
    logo=image,
    website='http://google.com',
    contactUser = userObj,
    supervisorContact = contact,
    # courses=[{
    #   'id':course,
    #   'action':'ADD'
    # }],
    hostingType=1,
    comments='Nil',
    status=2
  )
  print('Host Object genarated')
  return host.id

@pytest.fixture(scope='function',autouse=True)
def student(db,user):
  userObj = User.objects.get(id=user)
  student = Student.objects.create(
    user=userObj,
    comments='Nothing to comment',
    agencyName='Agency',
  )
  return student.id

#valid Class Data for testing
@pytest.fixture
def classValidData(course,instructor,host,location):
  data={
    'course':course,
    'instructor':instructor,
    'host':host,
    'location':location,
    'status':'Tentative',
    'type':'Open',
    'startDate':'2011-01-01',
    'endDate':'2012-02-01',
    'startTime':'00:00:00+05:30',
    'endTime':'00:00:00+05:30',
    "earlyFee": "120.00",
    "regularFee": "120.0",
    "lateFee": "125.0",
    "inServiceFee": "120.0",
    "inServiceSeats": 0,
    "onlineMeetingDetails": "string",
    "postedOnPTT": True,
    "orderDate": "2011-01-01",
    "orderDeliveryDate": "2011-01-01",
    "orderTrackingNumber": "AQBS4567$",
    "orderCarrier": "string",
    "orderQuantity": "1",
    "orderPrice": "125.0",
    "orderNotes": "string",
    "flightPrice": "126.2",
    "flightInfo": "string",
    "carRentalPrice": "200.0",
    "carRentalInfo": "string",
    "hotelPrice": "125.6",
    "hotelInfo": "string",
    "aar": [
      "string"
    ],
    }
  return data

@pytest.fixture
def classId(course,instructor,host,location):
  courseObj = Course.objects.get(id=course)
  instructorObj = Instructor.objects.get(id=instructor)
  hostObj=Host.objects.get(id=host)
  locationObj = Location.objects.get(id=location)
  data={
    'course':courseObj,
    'instructor':instructorObj,
    'host':hostObj,
    'location':locationObj,
    'status':3,
    'type':2,
    'startDate':'2011-01-01',
    'endDate':'2012-02-01',
    'startTime':'00:00:00+05:30',
    'endTime':'00:00:00+05:30',
    "earlyFee": "120.00",
    "regularFee": "120.0",
    "lateFee": "125.0",
    "inServiceFee": "120.0",
    "inServiceSeats": 0,
    "onlineMeetingDetails": "string",
    "postedOnPTT": True,
    "orderDate": "2011-01-01",
    "orderDeliveryDate": "2011-01-01",
    "orderTrackingNumber": "AQBS4567$",
    "orderCarrier": "string",
    "orderQuantity": "1",
    "orderPrice": "125.0",
    "orderNotes": "string",
    "flightPrice": "126.2",
    "flightInfo": "string",
    "carRentalPrice": "200.0",
    "carRentalInfo": "string",
    "hotelPrice": "125.6",
    "hotelInfo": "string",
    "aar": [
      "string"
    ],
    }
  classObj=Class.objects.create(**data)
  return classObj.id


  
@pytest.fixture
def classInvalidData(course,instructor,host,location):
  data={
    'instructor':instructor,
    'host':host,
    'location':location,
    "status":'Tentative',
    'type':'Open',
    'endDate':'2012-02-01',
    'startTime':'00:00:00+05:30',
    'endTime':'00:00:00+05:30',
    "regularFee": "120.0",
    "lateFee": "125.0",
    "inServiceFee": "120.0",
    "inServiceSeats": 0,
    "onlineMeetingDetails": "string",
    "postedOnPTT": True,
    "orderDate": "2011-01-01",
    "orderDeliveryDate": "2011-01-01",
    "orderTrackingNumber": "AQBS4567$",
    "orderCarrier": "string",
    "orderQuantity": "1",
    "orderPrice": "125.0",
    "orderNotes": "string",
    "flightPrice": "126.2",
    "flightInfo": "string",
    "carRentalPrice": "200.0",
    "carRentalInfo": "250",
    "hotelPrice": "125.6",
    "hotelInfo": "string",
    "aar": [
      "string"
    ],
    "adminNotes": [
      "string"
    ]
    }
  return data