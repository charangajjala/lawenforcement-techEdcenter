from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from meta.models import History

# Create your models here.

class PromoManager(models.Manager):
  def get_queryset(self):
      return super().get_queryset().filter(isDeleted=False)

class Promo(models.Model):
  class Type(models.IntegerChoices):
    SEATS = 1, _('Seats'),
    FLAT = 2, _('Flat'),
    PERCENTAGE = 3, _('Percentage'),
        
  code = models.CharField(max_length=255,unique=True)
  type = models.IntegerField(choices=Type.choices)
  value = models.CharField(max_length=255)
  singleUse = models.BooleanField()
  expiryDate = models.DateField()
  isActive = models.BooleanField(default=False)
  created = models.DateTimeField(auto_now_add=True)
  createdBy = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.DO_NOTHING,
    null = True,
    blank = True
  )
  isDeleted = models.BooleanField(default=False)
  history = models.ManyToManyField(History)
  objects = PromoManager()

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