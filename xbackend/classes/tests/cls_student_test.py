import pytest,json

from django.urls import reverse
from django.db.models.query_utils import Q

from rest_framework.status import *

from fixtures import *
from classes.models import Class,Roster

@pytest.mark.django_db
@pytest.mark.usefixtures('classId')
class TestClassStudentOperations:
  pass
#   def test_post_success(self,adminClient,classId,student):
#     response = adminClient.post(
#       reverse('move',args=(classId,)),
#       data={
#         'studentId':student,
#         'destClassId':classId,
#       },
#       format='json' 
#     )
#     classObj = Class.objects.get(id=classId)
#     assert response.status_code == HTTP_200_OK
#     assert len(Roster.objects.get(Q(student=student)&Q(cls=classObj))) != 0
    # def test_post_attendee_verification(self,client,classId):
    #     response = client.post(
    #       reverse('attendee_verification',args=(classId,)),
    #       format='json'
    #     )
    #     assert response.status_code == HTTP_400_BAD_REQUEST