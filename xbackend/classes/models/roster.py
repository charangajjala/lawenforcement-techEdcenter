from django.db import models

from students.models import Student
from .evaluation import Evaluation
from .invoice import Invoice
from .cls import Class
from meta.models import *

class RosterManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(isDeleted=False)

class Roster(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    cls = models.ForeignKey(Class, on_delete=models.DO_NOTHING)
    invoice = models.ForeignKey(Invoice, on_delete=models.DO_NOTHING)
    attendance = models.BooleanField(default=False)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.DO_NOTHING, null=True)
    isDeleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    history = models.ManyToManyField(History)
    objects=RosterManager()

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