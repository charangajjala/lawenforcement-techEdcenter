from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

from .managers import CourseManager
from .course import Course
from meta.models import *

class CertificationTrack(models.Model):
    title = models.CharField(max_length=255)
    shortName = models.CharField(max_length=10)
    logo = models.ForeignKey(
        File,
        on_delete=models.DO_NOTHING,
        null = True,
        blank = True
    )
    what = models.CharField(max_length=511, blank=True, null=True)
    why = models.CharField(max_length=511, blank=True, null=True)
    how = models.CharField(max_length=511, blank=True, null=True)
    maintainance = models.CharField(max_length=511, blank=True, null=True)
    
    who = ArrayField(models.CharField(max_length=511), default = None, null=True, blank=True)
    benefits = ArrayField(models.CharField(max_length=511), default=None, null=True, blank=True)
    requirements = ArrayField(models.CharField(max_length=511), default=None, null=True, blank=True)

    numCourses = models.IntegerField(default=0)
    requiredCourses = models.ManyToManyField(Course)
    optionalCourses = models.ManyToManyField(Course, related_name='+')

    isActive = models.BooleanField(default=False)
    isDeleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.DO_NOTHING,
        null = True,
        blank = True
    )
    history = models.ManyToManyField(History)

    objects = CourseManager()

    def toAdminDict(self):
        return dict(
            self.toDict(),
            isActive = self.isActive,
            created = self.created,
            createdBy = dict(
                id = self.createdBy.id,
                firstName = self.createdBy.firstName,
                lastName = self.createdBy.lastName
            ) if self.createdBy else None ,
            history = [h.toDict() for h in self.history.all()],
        )


    def toDict(self):
        return dict(
            id = self.id,
            title = self.title,
            shortName = self.shortName,
            what =self.what,
            why = self.why,
            who = self.who,
            benefits = self.benefits,
            how = self.how,
            requirements = self.requirements,
            maintainance = self.maintainance,
            numCourses = self.numCourses,
            requiredCourses = [c.toDict() for c in self.requiredCourses.all()],
            optionalCourses = [c.toDict() for c in self.optionalCourses.all()],
        )

    #def save(self, currentUser=None, *args, **kwargs):
    #    """
    #        1. update created by when new record created
     #   """
     #   if self._state.adding:
    #        self.createdBy = currentUser
#
     #   super().save(*args, **kwargs) 

    def update(self, oldValues, currentUser=None):

        for (field, oldValue) in oldValues.items():
            self.history.create(
                action = History.Action.UPDATE,
                field = field,
                oldValue = oldValue,
                createdBy = currentUser,
            )
        super().save()

    def delete(self, currentUser=None):
        self.isDeleted = True
        self.history.create(
            action = History.Action.DELETE,
            createdBy = currentUser
        )
        super().save()

    def __str__(self):
        return '{} - {}'.format(self.shortName, self.title)
