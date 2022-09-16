from django.utils.translation import gettext as _
from django.conf import settings
from django.db import models

from meta.models import *
from .manager import *

class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.ForeignKey(
        Address,
        on_delete = models.DO_NOTHING,
        default = None
    )
    seats = models.IntegerField()
    isWifiEnabled = models.BooleanField(default=False)
    isAudioEnabled = models.BooleanField(default=False)
    isProjectionEnabled = models.BooleanField(default=False)
    isMicEnabled = models.BooleanField(default=False)
    hasFlatScreens = models.BooleanField(default=False)

    locationContact = models.ForeignKey(
        Contact,
        on_delete = models.DO_NOTHING,
        default = None
    )
    closestAirports = models.TextField(default=None,null=True, blank=True)
    
    notes = models.TextField(default=None,null=True, blank=True)
    intel = models.ManyToManyField(Note,related_name='intel_set')
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
  
    objects = HostManager()

    def update(self, oldValues, currentUser=None):
        for (field, value) in oldValues.items():
            self.history.create(
                action = History.Action.UPDATE,
                field = field,
                oldValue = value,
                createdBy = currentUser
            )
        super().save()

    def delete(self, currentUser=None):
        self.isDeleted = True
        self.history.create(
            action = History.Action.DELETE,
            createdBy = currentUser
        )
        super().save()
