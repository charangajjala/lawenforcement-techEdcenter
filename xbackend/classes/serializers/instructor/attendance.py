from rest_framework import serializers

class AttendanceCodeRequest(serializers.Serializer):
  attendanceCode = serializers.IntegerField()

class UpdateStudentAttendance(serializers.Serializer):
  studentId = serializers.IntegerField()