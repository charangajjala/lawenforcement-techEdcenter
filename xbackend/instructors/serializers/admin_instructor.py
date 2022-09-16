from numpy import require
from rest_framework import serializers

from users.serializers import AddressRequest
from students.serializers import NoteResponse
from users.models import User
from meta.models import File,Action
from meta.serializers import ChoiceField
from courses.serializers import MaterialResponse

from datetime import datetime
import re
from django.utils.translation import gettext as _



class ContactRequest(serializers.Serializer):
    title = serializers.CharField(max_length=255,required=False)
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)
    email2 = serializers.EmailField(max_length=255,required=False, allow_blank=True)
    phone = serializers.CharField(max_length=30)
    phone2 = serializers.CharField(max_length=30,required=False, allow_blank=True)

    #name validation
    def validate_name(self,value):
        name = value
        regex = r"^[\w'\-,.]*[^_!¡?÷?¿\/\\+=@#$%ˆ&*(){}|~<>;:[\]]*$"

        if re.fullmatch(regex,name):
            return value
        else:
            raise serializers.ValidationError('Enter a valid Name')

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
        if len(value) == 0:
            return value
        else:
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
        phone = value
        if len(phone) == 0:
            return value
        else:
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

class FileRequest(serializers.Serializer):
    id = serializers.IntegerField()
    action = ChoiceField(choices=Action.choices)

    
    #docsid validation
    def validate_id(self,value):
        print('Id validation')
        try:            
            file = File.objects.get(id=value)  
            return value              
        except File.DoesNotExist:
            raise serializers.ValidationError('There was error in uploading the file')  

class NoteRequest(serializers.Serializer):
    text = serializers.CharField(max_length=255)
    #allowed chars A-z a-z ascii 32-176 10

    #action = serializers.ChoiceField(choices=Action.choices,write_only=True)

""" class ImageFileRequest(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    created = serializers.DateTimeField()

    def validate_id(self,value):
        print('Entering image id validation')
        try:
            fileobj=File.objects.get(id=value)
            return value
        except File.DoesNotExist:
            raise serializers.ValidationError('Requested File was not saved to databse')

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['createdBy'] = dict(
            id = instance.createdBy.id,
            firstName = instance.createdBy.firstName,
            lastName = instance.createdBy.lastName
        ) if instance.createdBy else None
        return res """

class InstructorRequest(serializers.Serializer):
    isActive = serializers.BooleanField(default=False)
    #nothing should be null & no null chars
    userId = serializers.IntegerField()
    #check if user exists
    image = serializers.IntegerField(required=False)
    #check if image exists in db
    dob = serializers.DateField(required=isActive)
    #check date
    #it should not be a future date
    ssn = serializers.CharField(max_length=255,required=isActive)
    #digits 9
    bio = serializers.CharField(required=isActive)
    #char limit 1000
    agencyName = serializers.CharField(max_length=255,required=isActive)
    agencyAddress = AddressRequest(required=isActive)
    agencyContact = ContactRequest(required=isActive)
    emergencyContact = ContactRequest(required=isActive)
    docs =FileRequest(many=True,allow_empty=True,required=False)
    #check if exits
    adminNotes = serializers.ListField(
        child=serializers.CharField(max_length=511),
        allow_empty=True,
        required=False
    )
    retiredDate =serializers.DateField(required=False)
    closestAirports = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    preferredAirports = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    travelNotes = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    #char limit 500

    #id validation
    def validate_userId(self,value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('User Does not exist')
        return value

    #imageid validation done in the request
    def validate_image(self,value):
        try:
            imageObj = File.objects.get(id=value)
            return value
        except File.DoesNotExist:
            raise serializers.ValidationError('Requested file was not uploaded try again')

    #dob validation
    def validate_dob(self,value):
        today = datetime.now()
        try:
            date = value.strftime('%Y-%m-%d')
            dob = datetime.strptime(date,'%Y-%m-%d')
            if today>=dob:
                return value
            else:
                raise serializers.ValidationError('Are you from the future....')
        except ValueError:
            raise serializers.ValidationError("Date should be in YYYY-MM-DD")

    #ssn validation
    def validate_ssn(self,value):
        #made into groups decide whichever necessary or else keep all
        regex = (r"^(?!123([ -]?)45([ -]?)6789)(?!\b(\d)\3+\b)(?!000|666|900|999)[0-9]{3}([ -]?)(?!00)[0-9]{2}\4(?!0000)[0-9]{4}$")

        if re.fullmatch(regex,value):
            return value
        else:
            raise serializers.ValidationError('Enter a valid ssn number')

    #text area validation
    def validate_bio(self,value):
        global chars
        chars=0
        regex = r"(?s)((?:[^\n][\n]?)+)"
        
        try:
            for match in re.finditer(regex,value,re.MULTILINE):
                chars = match.end()
            if chars>1000:
                raise serializers.ValidationError('Total charachters must not exceed 1000')
            else:
                return value
        except ValueError:
            raise serializers.ValidationError('Data enterd is not allowed on here')

    #text area validation
    def validate_travelNotes(self,value):
        global chars
        chars=0
        regex = r"(?s)((?:[^\n][\n]?)+)"
        
        try:
            for match in re.finditer(regex,value,re.MULTILINE):
                chars = match.end()
            if chars>500:
                raise serializers.ValidationError('Total charachters must not exceed 1000')
            else:
                return value
        except ValueError:
            raise serializers.ValidationError('Data enterd is not allowed on here')


class InstructorResponse(InstructorRequest):
    id = serializers.IntegerField()
    image = serializers.SerializerMethodField()
    userId = serializers.SerializerMethodField('get_userId')
    isDeleted = serializers.BooleanField(default=False)
    created = serializers.DateTimeField()
    docs = MaterialResponse(many=True,allow_empty=True)
    adminNotes = NoteResponse(many=True,allow_empty=True,required=False)

    def get_image(self,instance):
        return instance.id

    def get_userId(self,instance):
        return instance.user.id
    
    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['createdBy'] = dict(
            id = instance.createdBy.id,
            firstName = instance.createdBy.firstName,
            lastName = instance.createdBy.lastName
        ) if instance.createdBy else None
        res['history'] = [h.toDict() for h in instance.history.all()]
        return res

class UserListResponse(serializers.Serializer):
    id = serializers.IntegerField()
    firstName = serializers.SerializerMethodField()
    lastName = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    isActive = serializers.BooleanField(default=False)

    def get_firstName(self,instance):
        return instance.user.firstName

    def get_lastName(self,instance):
        return instance.user.lastName

    def get_email(self,instance):
        return instance.user.email
    
    def get_phone(self,instance):
        return instance.user.phone