from rest_framework import serializers
from courses.models import Topic

import re

class AdminTopicRequest(serializers.Serializer):
    name = serializers.CharField(max_length=255)

    def validate_name(self,value):
        regex = r"(?:[a-zA-Z\- :0-9!@#$%^&*():;'\",.><?\[\]\}\{])+"
        
        if re.fullmatch(regex,value):
            return value
        else:
            raise serializers.ValidationError('The name of the topic contains invalid characters')

class AdminTopicResponse(AdminTopicRequest):
    id = serializers.IntegerField()
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
