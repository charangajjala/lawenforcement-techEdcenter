from django.db import models
from django.conf import settings

from meta.models import *
from .manager import *

class Instructor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete = models.DO_NOTHING,
    )
    image = models.ForeignKey(File, related_name='+', on_delete=models.DO_NOTHING, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    ssn = models.CharField(max_length=255, default=None, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    agencyName  = models.CharField(max_length=255,default=None, null=True, blank=True)
    agencyAddress = models.ForeignKey(Address, on_delete=models.DO_NOTHING, null=True, blank=True)
    agencyContact = models.ForeignKey(Contact, related_name='+',on_delete=models.DO_NOTHING, null=True, blank=True)
    emergencyContact = models.ForeignKey(Contact, on_delete=models.DO_NOTHING, null=True, blank=True)

    retiredDate = models.DateField(default=None)
    closestAirports = models.TextField(null=True, blank=True)
    preferredAirports = models.TextField(null=True, blank=True)
    travelNotes = models.TextField(null=True, blank=True)

    docs = models.ManyToManyField(File)
    adminNotes = models.ManyToManyField(Note)

    isActive = models.BooleanField(default=False)
    isDeleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.DO_NOTHING,
        related_name = '+',
        blank = True,
        null = True
    )
    history = models.ManyToManyField(History)
  
    objects = InstructorManager()
    
    def update(self, oldValues, currentUser=None):

        for (field, oldValue) in oldValues.items():
            self.history.create(
                action = History.Action.UPDATE,
                field = field,
                oldValue = oldValue,
                createdBy = currentUser,
            )
        super().save()  # Call the "real" save() method.

    def delete(self, currentUser=None):
        """
            Custom method to accomplish following
            3. update history when record deleted
        """
        self.isDeleted = True

        self.history.create(
            action = History.Action.DELETE,
            createdBy = currentUser,
        )
        super().save()

