from django.contrib.postgres.fields.array import ArrayField
from django.db import models
from django.conf import settings

from meta.models import *
from .studentmanager import *

class Student(models.Model):
  user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete = models.DO_NOTHING,
    )
  docs = models.ManyToManyField(File)
  comments = models.CharField(max_length=511, null=True, blank=True)
  agencyName = models.CharField(max_length=255)
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
  objects = StudentManager()

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
          createdBy = currentUser,
      )
      super().save()