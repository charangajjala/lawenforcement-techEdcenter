from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext as _


class Agenda(models.Model):
    value = ArrayField(models.CharField(max_length=255))
    day = models.PositiveIntegerField()

    isDeleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.DO_NOTHING,
        null = True,
        blank = True
    )

    def toDict(self):
        return dict(
            id = self.id,
            value = self.value,
            day = self.day
        )

    def toAdminDict(self):
        return dict(
            self.toDict(),
            created = self.created,
            createdBy = dict(
                id = self.createdBy.id,
                firstName = self.createdBy.firstName,
                lastName = self.createdBy.lastName
            ) if self.createdBy else None
        )

