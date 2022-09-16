from rest_framework import serializers

class MoveStudent(serializers.Serializer):
  studentId=serializers.IntegerField()
  destClassId=serializers.IntegerField()

class RemoveStudent(serializers.Serializer):
  studentId=serializers.IntegerField()

class SubstituteStudent(serializers.Serializer):
  studentId=serializers.IntegerField()
  newStudentId=serializers.IntegerField()