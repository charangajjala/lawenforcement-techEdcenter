from rest_framework.serializers import SerializerMethodField,ChoiceField

class GetFieldData(SerializerMethodField):

  def bind(self,field_name,parent):
    super(SerializerMethodField,self).bind(field_name,parent)

  def to_representation(self, value):
    return self.method_name(value)

class ChoiceField(ChoiceField):
    def to_representation(self, data):
        if data not in self.choices.keys():
            print('data : ',data)
            self.fail('invalid_choice', input=data)
        else:
            return self.choices[data]

    def to_internal_value(self, data):
        for key, value in self.choices.items():
            if value == data:
                 return value
        self.fail('invalid_choice', input=data)

class ChoiceField2(ChoiceField):
    def to_representation(self, data):
        if data not in self.choices.keys():
            print('data : ',data)
            self.fail('invalid_choice', input=data)
        else:
            return self.choices[data]

    def to_internal_value(self, data):
        for key, value in self.choices.items():
            if value == data:
                return key
        self.fail('invalid_choice', input=data)

