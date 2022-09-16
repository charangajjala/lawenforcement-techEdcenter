from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import JSONParser

from users.models import User

import re

class AddressRequest(serializers.Serializer):
    address1 = serializers.CharField(max_length=255)
    address2 = serializers.CharField(max_length=255, required=False)
    #allowed chars A-z,a-z,0-9,',','/','-','.','#'
    city = serializers.CharField(max_length=255)
    #allowed chars A-Z,a-z,' ','',-
    state = serializers.CharField(max_length=10)
    #allowed chars: 2
    zip = serializers.CharField(max_length=10)
    #digits 5

    """
     re.fullmatch(r"?:[A-Z][A-Z- ]",state):
        print('state is validated') """

    #address validation
    def validate_address1(self,value):
        regex = r"\d+[ ](?:[A-Za-z0-9.-]+[ ]?)+"

        if re.fullmatch(regex,value):
            return value
        else:
            raise serializers.ValidationError('Enter the address in right format')

    def validate_address2(self,value):
        regex = r"\d+[ ](?:[A-Za-z0-9.-]+[ ]?)+"

        if re.fullmatch(regex,value):
            return value
        else:
            raise serializers.ValidationError('Enter the address in right format')

    #zip validation
    def validate_zip(self,value):
        regex = r"^\d{5}(?:[-\s]\d{4})?$"

        if re.fullmatch(regex,value):
            return value
        else:
            raise serializers.ValidationError('Enter a valid zipcode')

    #city Validation
    def validate_city(self,value):
        regex = r"^([a-zA-Z]+(?:. |-| |'))*[a-zA-Z]*$"
        #if wanted to we can adjust the way to represent re.finditer cuz it has groups        
        if re.fullmatch(regex,value):
            return value
        else:
            raise serializers.ValidationError('Enter a valid city name')

    #state validation
    #i hope its not required


class UserRequest(serializers.Serializer):
    title = serializers.CharField(max_length=255,)
    firstName = serializers.CharField(max_length=255)
    lastName = serializers.CharField(max_length=255)
    #allowed chars A-Z,a-z,' ','',-,
    email = serializers.EmailField()
    #all lowercases 
    phone = serializers.CharField(max_length=255)
    email2 = serializers.EmailField(required=False,allow_null=True)
    phone2 = serializers.CharField(max_length=255,required=False,allow_null=True)
    isAdmin = serializers.BooleanField(default=False)
    isSuperUser = serializers.BooleanField(default=False)
    address = AddressRequest()
    password = serializers.CharField(max_length=255)

    #first name
    def validate_firstName(self,value):
        fname = value
        regex = r"^[\w'\-,.]*[^_!¡?÷?¿\/\\+=@#$%ˆ&*(){}|~<>;:[\]]*$"

        if re.fullmatch(regex,fname):
            return value
        else:
            raise serializers.ValidationError('Enter a valid First Name')

    def validate_lastName(self,value):
        lname = value
        regex = r"^[\w'\-,.]*[^_!¡?÷?¿\/\\+=@#$%ˆ&*(){}|~<>;:[\]]*$"

        if re.fullmatch(regex,lname):
            return value
        else:
            raise serializers.ValidationError('Enter a valid First Name')


    #email Validation
    def validate_email(self,value):
        email=value.lower()
        #add additional extensions if any
        regex = r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:[A-Z]{2}|com|org|)\b"

        if re.fullmatch(regex,email,re.MULTILINE):
            #checking data base with this email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return email
            raise serializers.ValidationError("given email {} is already in use".format(email))
            
        else:
            raise serializers.ValidationError('Enter a valid email Address')

    def validate_email2(self,value):
        email=value.lower()
        #add additional extensions if any
        regex = r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:[A-Z]{2}|com|org|)\b"

        if re.fullmatch(regex,email,re.MULTILINE):
            print('Email is valid')
            return email
        else:
            raise serializers.ValidationError('Enter a valid email Address')

    #phone Validation
    def validate_phone(self,value):
        print('Entering Phone Validation')
        phone = value
        regex = r"^(?:(?:\(?(?:00|\+)([1-4]\d\d|[1-9]\d?)\)?)?[\-\.\ \\\/]?)?((?:\(?\d{1,}\)?[\-\.\ \\\/]?){0,})(?:[\-\.\ \\\/]?(?:#|ext\.?|extension|x)[\-\.\ \\\/]?(\d+))?$"

        matchObj = re.finditer(regex, phone, re.MULTILINE)

        if matchObj:
            for matchNum,match in enumerate(matchObj,start=1):
                #edit phone number pattern if necessary
                match = match.group()
                if phone==match:
                    return phone
            
        else:
            raise serializers.ValidationError('Enter a valid phone number')
    
    def validate_phone2(self,value):
        print('Entering Phone Validation')
        phone = value
        regex = r"^(?:(?:\(?(?:00|\+)([1-4]\d\d|[1-9]\d?)\)?)?[\-\.\ \\\/]?)?((?:\(?\d{1,}\)?[\-\.\ \\\/]?){0,})(?:[\-\.\ \\\/]?(?:#|ext\.?|extension|x)[\-\.\ \\\/]?(\d+))?$"

        matchObj = re.finditer(regex, phone, re.MULTILINE)

        if matchObj:
            for matchNum,match in enumerate(matchObj,start=1):
                #edit phone number pattern if necessary
                match = match.group()
                if phone==match:
                    return phone
            
        else:
            raise serializers.ValidationError('Enter a valid phone number')

    #password Validation
    def validate_password(self,value):
        password = value
        flag=0
        while True:  
            if (len(password)<8):
                flag = -1
                break
            elif not re.search("[a-z]", password):
                flag = -1
                break
            elif not re.search("[A-Z]", password):
                flag = -1
                break
            elif not re.search("[0-9]", password):
                flag = -1
                break
            elif not re.search("\W", password):
                flag = -1
                break
            elif re.search("\s", password):
                flag = -1
                break
            else:
                flag = 0
                print("Valid Password")
                break
        if flag==0:
            return password

        if flag ==-1:
            raise ValidationError('Password does not match the required qualifications')


class UserListResponse(serializers.ListSerializer):
    def to_representation(self, data):
        print(data)
        return [
            dict(
                id = i.id,
                name = '{} {}'.format(i.firstName, i.lastName),
                email = i.email,
                isAdmin = i.isAdmin,
                isSuperUser = i.isSuperUser
            ) for i in data
        ]

class UserResponse(UserRequest):
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

#    class Meta:
#        list_serializer_class = UserListResponse
        
class UserResponse2(serializers.Serializer):
    id = serializers.IntegerField()
    firstName = serializers.CharField(max_length=255)
    lastName = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=255, required=False, allow_null=True)
    isAdmin = serializers.BooleanField(default=False)
    isSuperUser = serializers.BooleanField(default=False)