from django.utils.translation import gettext as _
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models

from meta.models import *
from courses.models import Course

from .location import *
from .manager import *

class Host(models.Model):
    class Status(models.IntegerChoices):
        RECEIVED = 1, _('Received')
        REVIEW = 2, _('In-Review')
        DEFER  = 3, _('Deferred')
        SHORTLIST = 4, _('Shortlisted')
        REJECT = 5, _('Rejected')
        ONBOARDING = 6, _('Onboarding')
        LOA = 7, _('LOA')
        SIGNED = 8, _('Signed')

    class Type(models.IntegerChoices):
        OPEN = 1, _('Open')
        INSERVICE = 2, _('In-Service')
        CONFERENCE = 3, _('Conference')
        SPEAKER = 4, _('Speaker')
        SPLIT = 5, _('Split')
        # WEBINAR = 6, _('Webinar')
        # VIRTUAL =7, _('Virtual')

    name = models.CharField(max_length=255)
    website = models.URLField(default=None)
    contactUser = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete = models.DO_NOTHING,
    )
    address = models.ForeignKey(
        Address,
        on_delete = models.DO_NOTHING,
        default = None
    )
    logo = models.ForeignKey(
        File,
        related_name='logo',
        on_delete = models.DO_NOTHING,
        default = None,
        null = True
    )
    supervisorContact = models.ForeignKey(
        Contact,
        on_delete = models.DO_NOTHING,
        default = None
    )

    hostingType = models.IntegerField(choices=Type.choices,default=1)
    status = models.IntegerField(choices=Status.choices,default=1)
    comments = models.TextField(default=None)
    
    courses = models.ManyToManyField(Course)
    locations = models.ManyToManyField(Location)
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
  
    objects = HostManager()

    def update(self, oldValues, currentUser=None):
        print('These are the old values : ',oldValues)
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
