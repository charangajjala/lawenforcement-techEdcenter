from django.utils.translation import gettext as _
from django.conf import settings
from django.db import models

class Action(models.IntegerChoices):
    ADD = 1, _('ADD')
    REMOVE = 2, _('REMOVE')

class Action2(models.IntegerChoices):
    ADD = 1, _('ADD')
    REMOVE = 2, _('DELETE')

class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='static/material/')
    
    isDeleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.DO_NOTHING,
        null = True,
        blank = True
    )

    def toAdminDict(self):
        return dict(
            id = self.id,
            name = self.file.name,
            url = self.file.url,
            created = self.created,
            createdBy = dict(
                id = self.createdBy.id,
                firstName = self.createdBy.firstName,
                lastName = self.createdBy.lastName
            ) if self.createdBy else None
        )


class Address(models.Model):
    address1 = models.CharField(max_length=255, null=True)
    address2 = models.CharField(max_length=255,null=True,blank=True)
    city = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=10, null=True)
    zip = models.CharField(max_length=10, null=True)

class History(models.Model):
    class Action(models.IntegerChoices):
        ADD = 1, _('Add')
        UPDATE = 2, _('Update')
        DELETE = 3, _('Delete')

    action = models.IntegerField(choices = Action.choices)
    field = models.CharField(max_length=255, null=True)
    oldValue = models.CharField(max_length=255, null=True)
    created = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name = '+',
        null=True,
        blank=True
    )
    
    def toDict(self):
        """
            Returns a Python dict of user history object
        """
        return dict(
            action = self.get_action_display(),
            field = self.field,
            oldValue = self.oldValue,
            created = self.created,
            createdBy = dict(
                id = self.createdBy.id,
                firstName = self.createdBy.firstName,
                lastName = self.createdBy.lastName
            ) if self.createdBy else None

)
class Contact(models.Model):
    title = models.CharField(max_length=255,null=True,blank=True,default=None)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    email2 = models.EmailField(max_length=255,null=True,blank=True,default=None)
    phone = models.CharField(max_length=30)
    phone2 = models.CharField(max_length=30,null=True,blank=True,default=None)

class Note(models.Model):
    text = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.DO_NOTHING,
        blank = True,
        null = True
    )
