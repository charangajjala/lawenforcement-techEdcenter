from rest_framework import serializers
from courses.serializers import OperationRequest
from courses.models import Course

class CourseTitleResponse(serializers.Serializer):
  id = serializers.IntegerField()
  title = serializers.CharField(max_length=255)

class TrackRequest(serializers.Serializer):
  isActive=serializers.BooleanField(default=False)
  title = serializers.CharField(max_length=255,required=True)
  shortName = serializers.CharField(max_length=10,required=isActive)
  logo = serializers.IntegerField(required=isActive)

  what = serializers.CharField(max_length=255,required=isActive)
  why = serializers.CharField(max_length=255,required=isActive)
  how = serializers.CharField(max_length=255,required=isActive)
  maintainance = serializers.CharField(max_length=255,required=isActive)

  who = serializers.ListField(
    child = serializers.CharField(max_length=255),
    allow_empty = True,
    required=isActive
  )    
  benefits = serializers.ListField(
    child = serializers.CharField(max_length=255),
    allow_empty = True,
    required=isActive
  )
  requirements = serializers.ListField(
    child = serializers.CharField(max_length=255),
    allow_empty = True,
    required=isActive
  )

  numCourses = serializers.IntegerField(required=isActive)

  requiredCourses = OperationRequest(
    many=True,
    allow_empty=True,
    required=isActive
    )

  optionalCourses = OperationRequest(
    many=True,
    allow_empty=True,
    required=isActive
    )  

class TrackResponse(TrackRequest):

  id = serializers.IntegerField()
  isDeleted = serializers.BooleanField(default=False)
  created = serializers.DateTimeField()
  requiredCourses = CourseTitleResponse(
    many=True,
    allow_empty=True,
    required=False
  )
  optionalCourses = CourseTitleResponse(
    many=True,
    allow_empty=True,
    required=False
  )

  def to_representation(self, instance):
    res = super().to_representation(instance)
    res['createdBy'] = dict(
        id = instance.createdBy.id,
        firstName = instance.createdBy.firstName,
        lastName = instance.createdBy.lastName
    ) if instance.createdBy else None
    res['logo'] = instance.logo.file.url if instance.logo else None
    res['history'] = [h.toDict() for h in instance.history.all()]
    return res

class TracksListResponse(serializers.Serializer):
  id = serializers.IntegerField()
  title = serializers.CharField(max_length=255)
  shortName = serializers.CharField(max_length=10)
  numCourses = serializers.IntegerField()
  isActive = serializers.BooleanField(default=False)
  created = serializers.DateTimeField()

class TrackCourseResponse(serializers.Serializer):
  requiredCourses = CourseTitleResponse(
    many=True,
    allow_empty=True,
    required=False
  )
  optionalCourses = CourseTitleResponse(
    many=True,
    allow_empty=True,
    required=False
  )
  