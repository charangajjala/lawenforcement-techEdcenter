from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from datetime import time

from courses.models import Course
from instructors.models import Instructor
from hosts.models import Host, Location
from meta.models import *
from classes.models.invoice import Invoice

class ClassManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(isDeleted=False)

class Class(models.Model):
    class Status(models.IntegerChoices):
        TENTATIVE = 1, _('Tentative'),
        BOOKED = 2, _('Booked'),
        CONFIRMED = 3, _('Confirmed'),
        CLOSED = 4, _('Closed'),
        CANCELLED = 5, _('Cancelled'),

    class Type(models.IntegerChoices):
        OPEN = 1, _('Open')
        INSERVICE = 2, _('In-Service'),
        CONFERENCE = 3, _('Conference'),
        SPEAKER = 4, _('Speaker'),
        #WEBINAR = 5, _('Webinar'),
        SPLIT = 6, _('Split'),
    
    class DeliveryType(models.IntegerChoices):
        ONLINE = 1, _('Online'),
        OFFLINE = 2, _('Offline')

    course = models.ForeignKey(Course, on_delete=models.PROTECT, null=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.PROTECT, null=True)
    host = models.ForeignKey(Host, on_delete=models.PROTECT, null=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, null=True)

    inServiceInvoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, null=True)    
    inServiceFee = models.DecimalField(max_digits=19, decimal_places=2, default=None,null=True)
    inServiceSeats = models.PositiveIntegerField(null=True, blank=True)
    
    status = models.IntegerField(choices = Status.choices)
    type = models.IntegerField(choices = Type.choices)
    deliveryType = models.IntegerField(choices = DeliveryType.choices)
    
    startDate = models.DateField(default=None)
    endDate = models.DateField(default=None)
    startTime = models.TimeField(default=time(hour=8,minute=0))
    endTime = models.TimeField(default=time(hour=16,minute=0))
    earlyFee = models.DecimalField(max_digits=19, decimal_places=2, default=None)
    regularFee = models.DecimalField(max_digits=19, decimal_places=2, default=None)
    lateFee = models.DecimalField(max_digits=19, decimal_places=2, default=None)
    onlineMeetingDetails = models.CharField(max_length=255, blank=True, null=True)
    postedOnPTT = models.BooleanField(default=False)

    orderDate = models.DateField(blank=True, null=True)
    orderDeliveryDate = models.DateField(blank=True, null=True)
    orderTrackingNumber = models.CharField(max_length=30, blank=True, null=True)
    orderCarrier = models.CharField(max_length=30, blank=True, null=True)
    orderQuantity = models.PositiveIntegerField(blank=True, null=True)
    orderPrice = models.DecimalField(max_digits=19, decimal_places=2, default=None,null=True)
    orderNotes = models.CharField(max_length=255, blank=True, null=True)
    flightPrice = models.DecimalField(max_digits=19, decimal_places=2, default=None,null=True)
    flightInfo = models.TextField(blank=True, null=True)
    carRentalPrice = models.DecimalField(max_digits=19, decimal_places=2, default=None,null=True)
    carRentalInfo = models.TextField(blank=True, null=True)
    hotelPrice = models.DecimalField(max_digits=19, decimal_places=2, default=None,null=True)
    hotelInfo = models.TextField(blank=True, null=True)

    docs = models.ManyToManyField(File)
    adminDocs = models.ManyToManyField(File,related_name='admin_docs')
    aar = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    attendanceCode = models.IntegerField(default=None,blank=True, null=True)
    adminNotes = models.ManyToManyField(Note)
    
    isActive = models.BooleanField(default=False)
    isDeleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    history = models.ManyToManyField(History)
    objects=ClassManager()

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