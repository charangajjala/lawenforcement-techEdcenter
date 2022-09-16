from re import L
from django.db import models
from django.utils.translation import gettext_lazy as _
from meta.models import *
from promos.models import Promo

class InvoiceManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(isDeleted=False)

class Invoice(models.Model):        

    class PayMethod(models.IntegerChoices):
        #PURCHASEORDER = 1, _('Purchase Order'),
        CARD = 1, _('Credit Card'),
        PAYLATER = 2, _('Pay Later'),
        #CHECK = 3, _('Check'),
        #EFT = 4, _('EFT/ACH'),
    class InvoiceType(models.IntegerChoices):
        REGISTRATION = 1, _('Registration'),
        INSERVICE = 2, _('Inservice'),
        CUSTOM = 3, _('Custom'),

    promo = models.ForeignKey(Promo, on_delete=models.DO_NOTHING,null=True,blank=True)
    
    #it was initially unique but to complete the process made it numb
    invoiceNum = models.PositiveIntegerField(unique=True)
    accessKey = models.CharField(max_length=50)
    #removed the class (cls) link added it to class as contract invoice
    pmrAgency = models.CharField(max_length=100, null=True, blank=True)
    pmrContact = models.ForeignKey(Contact,on_delete=models.DO_NOTHING)
    pmrAddress = models.ForeignKey(Address,on_delete=models.DO_NOTHING)

    type = models.IntegerField(choices = InvoiceType.choices)
    paymentMethod = models.IntegerField(choices = PayMethod.choices, default=None)
    #remove it in the next db creation
    transactionId = models.CharField(max_length=100,default=None,blank=True,null=True)
    paid = models.BooleanField()
    paidDate = models.DateField(blank=True, null=True)
    refund = models.BooleanField(default=False)
    refundDate = models.DateField(default=None, null=True, blank=True)
    refundNotes = models.CharField(max_length=255, blank=True, null=True)
    
    #initially it was not numb
    price = models.DecimalField(max_digits=19, decimal_places=2,null=True, blank=True)
    totalPrice = models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True)
    purchaseOrder = models.CharField(max_length=30, blank=True, null=True)
    checkNumber = models.CharField(max_length=15, blank=True, null=True)
    eftAch = models.CharField(max_length=20, blank=True, null=True)
    card = models.CharField(max_length=30, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    isDeleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add = True)
    createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    objects = InvoiceManager()
    history = models.ManyToManyField(History)

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
