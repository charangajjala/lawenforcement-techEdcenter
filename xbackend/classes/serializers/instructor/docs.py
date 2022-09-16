from django.forms.models import model_to_dict
from rest_framework import serializers
from meta.serializers import ChoiceField,GetFieldData
from meta.models import Action2

class DocsRequest(serializers.Serializer):
  action = ChoiceField(choices = Action2.choices,write_only=True)
  id = serializers.IntegerField()

class DocsUploadRequest(serializers.Serializer):
  docs = DocsRequest(many=True)

class DocResponse(serializers.Serializer):
  id =serializers.IntegerField()
  name = serializers.CharField()
  url = GetFieldData(lambda obj:obj.file.url)

class CourseDocsResponse(serializers.Serializer):
  courseId = GetFieldData(lambda obj:obj.id)
  title = GetFieldData(lambda obj:obj.title)
  docs = GetFieldData(lambda obj:list(obj.material.values()))