from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from meta.models import History

class HoursManager(models.Manager):
  def get_queryset(self):
      return super().get_queryset().filter(isDeleted=False)

# Create your models here.
class Hours(models.Model):
  class Type(models.IntegerChoices):
    VACATION = 1,_('Vacation')
    UNPLANNED = 2,_('Unplanned')
    HOLIDAY=3,_('Holiday')

  date = models.DateField()
  type = models.IntegerField(choices = Type.choices)
  hours = models.IntegerField()
  created = models.DateTimeField(auto_now_add=True)
  isDeleted = models.BooleanField(default=False)
  createdBy = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.DO_NOTHING,
    related_name='madeby',
    null = True,
    blank = True
  )
  history = models.ManyToManyField(History)
  objects=HoursManager()

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