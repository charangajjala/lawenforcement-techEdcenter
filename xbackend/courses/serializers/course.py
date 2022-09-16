from rest_framework import serializers
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext as _

from courses.models import *
from meta.serializers import ChoiceField

class Action(models.IntegerChoices):
    ADD = 1, _('ADD')
    REMOVE = 2, _('DELETE')

class AgendaRequest(serializers.Serializer):
    value = serializers.ListField(child=serializers.CharField(max_length=255))
    day = serializers.IntegerField()

#class FileRequest(serializers.Serializer):

class OperationRequest(serializers.Serializer):
    id=serializers.IntegerField()
    action = ChoiceField(choices=Action.choices, write_only=True)

class MaterialResponse(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255, read_only=True)
    url = serializers.CharField(max_length=255, read_only=True)

class TopicResponse(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255,read_only=True)

class CourseRequest(serializers.Serializer):
    isActive = serializers.BooleanField(default=False)
    courseNum = serializers.CharField(max_length=10)
    title = serializers.CharField(max_length=255, required=isActive)
    subTitle = serializers.CharField(max_length=255, required=isActive)
    shortDesc = serializers.CharField(max_length=255, required=isActive)
    days = serializers.IntegerField(required = isActive)
    targetAudience = serializers.CharField(max_length=255, required=isActive)
    prerequisites = serializers.CharField(max_length=255, required=isActive)
    isNew = serializers.BooleanField(default=False)
    description = serializers.ListField(
        child=serializers.CharField(max_length=511),
        allow_empty=True,
        required=isActive
    )

    topic = OperationRequest(
        many=True,
        allow_empty=True,
        required=False
    )
    material = OperationRequest(
        many=True,
        allow_empty=True,
        required=False
    )
    agenda = AgendaRequest(
        allow_empty=True,
        many=True,
        required=False
    )

    def validate_courseNum(self,value):
        courseNum = value
        try:
            courseNumObj = Course.objects.get(courseNum=courseNum)
        except Course.DoesNotExist:
            return value
        raise serializers.ValidationError('Course Number already exists')



class CourseResponse(CourseRequest):
    id = serializers.IntegerField()
    topic = TopicResponse(
        many=True,
        allow_empty=True,
        required=False
    )
    material = MaterialResponse(
        many=True,
        allow_empty=True,
        required=False
    )
    isDeleted = serializers.BooleanField()
    created = serializers.DateTimeField()

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['createdBy'] = dict(
            id = instance.createdBy.id,
            firstName = instance.createdBy.firstName,
            lastName = instance.createdBy.lastName
        ) if instance.createdBy else None
        res['history'] = [h.toDict() for h in instance.history.all()]
        return res

