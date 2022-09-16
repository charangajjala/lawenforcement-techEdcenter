from django.utils.translation import gettext as _
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models

from meta.models import *
from courses.models import Course
from .manager import *
from courses.models import Course

class Applicant(models.Model):
    class Status(models.IntegerChoices):
        RECEIVED = 1, _('RECEIVED')
        REVIEW = 2, _('REVIEW')
        DEFER  = 3, _('DEFER')
        SHORTLIST = 4, _('SHORTLIST')
        REJECT = 5, _('REJECT')
        ONBOARDING = 6, _('ONBOARDING')
        HIRED = 7, _('HIRED')

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete = models.DO_NOTHING,
    )

    status = models.IntegerField(choices=Status.choices,default=1)
    comments = models.CharField(max_length=511, null=True, blank=True)
    coursePreferences = models.ManyToManyField(Course)
    docs = models.ManyToManyField(File)
    adminNotes = models.ManyToManyField(Note)
    
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

    def update(self,oldValues, currentUser=None):
        
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
