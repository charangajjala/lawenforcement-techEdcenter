from rest_framework import serializers

class ClassEvaluationRequest(serializers.Serializer):
  q1 = serializers.IntegerField(default=0)
  q2 = serializers.IntegerField(default=0)
  q3 = serializers.IntegerField(default=0)
  q4 = serializers.IntegerField(default=0)
  q5 = serializers.IntegerField(default=0)
  q6 = serializers.IntegerField(default=0)
  q7 = serializers.IntegerField(default=0)
  q8 = serializers.IntegerField(default=0)
  q9 = serializers.IntegerField(default=0)

  q10 = serializers.BooleanField(default=False)
  q11 = serializers.BooleanField(default=False)
  q12 = serializers.BooleanField(default=False)

  comments = serializers.CharField(required=False)
  interest = serializers.CharField(required=False)

  def to_representation(self, instance):
      res = super().to_representation(instance)
      if self.context.get('studentId'):
        res['id'] = self.context.get('studentId')
      if instance.student.id:
        res['id'] = instance.student.id
      return res

class EvalutionResponse(serializers.Serializer):
  q1 = serializers.IntegerField()
  q2 = serializers.IntegerField()
  q3 = serializers.IntegerField()
  q4 = serializers.IntegerField()
  q5 = serializers.IntegerField()
  q6 = serializers.IntegerField()
  q7 = serializers.IntegerField()
  q8 = serializers.IntegerField()
  q9 = serializers.IntegerField()

  q10 = serializers.BooleanField()
  q11 = serializers.BooleanField()
  q12 = serializers.BooleanField()

  comments = serializers.CharField(required=False)
  interest = serializers.CharField(required=False)

  def to_representation(self, instance):
      res = super().to_representation(instance)
      id = self.context.get('studentId')
      if id:
        res['id'] = self.context.get('studentId')
      return res


