from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from meta.models import Address, History

class MyUserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(isDeleted=False)

class User(AbstractBaseUser):
    title = models.CharField(max_length=255, null=True,blank=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    # class UiRoles(models.IntegerChoices):
    #     INSTRUCTOR = 1, _('Instructor')
    #     HOST = 2, _('Host')
    #     APPLICANT = 3, _('Applicant')
    #     ATTENDEE = 4, _('Attendee')
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email2 = models.EmailField(max_length=255, null=True, blank=True)
    phone2 = models.CharField(max_length=255, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, null=True)
    isAdmin = models.BooleanField(default=False)
    isSuperUser = models.BooleanField(default=False)

    isDeleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(
        'self',
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )
    history = models.ManyToManyField(History)

    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName', 'password']

    def clean(self):
        if self.isAdmin == True and self.isSuperUser == True:
            raise ValidationError('Not Possible')

    def save(self, *args, **kwargs):
        print("<---- users.models.User.save ---->")
        # self.full_clean()
        if self._state.adding:
            self.set_password(self.password)
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def update(self, oldValues, currentUser=None):
        # self.full_clean()
        if 'password' in oldValues:
            self.set_password(self.password)

        for (field, oldValue) in oldValues.items():
            self.history.create(
                action = History.Action.UPDATE,
                field = field,
                oldValue = oldValue,
                createdBy = currentUser,
            )
        super().save()  # Call the "real" save() method.

    def delete(self, currentUser=None):
        self.isDeleted = True
        self.history.create(
            action = History.Action.DELETE,
            createdBy = currentUser
        )
        super().save()

    # Custom model methods
    def toDict(self):
        """
            Returns a proper Python dict of user
        """
        return dict(
            id = self.id,
            firstName = self.firstName,
            lastName = self.lastName,
            email = self.email,
            password = self.password,
            isAdmin = self.isAdmin,
            isSuperUser = self.isSuperUser,
            created = self.created,
            createdBy = dict(
                id = self.createdBy.id,
                firstName = self.createdBy.firstName,
                lastName = self.createdBy.lastName
            ) if self.createdBy else None,
            history = [h.toDict() for h in self.history.all()]
        )

    @property
    def is_staff(self):
        return self.isAdmin or self.isSuperUser

    @property
    def is_admin(self):
        return self.isAdmin

    @property
    def is_superuser(self):
        return self.isSuperUser

    def __str__(self):
        return '{} {} {}'.format(self.firstName, self.lastName, self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
