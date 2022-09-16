from django.db import models
from django.conf import settings

from meta.models import History

class TopicManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(isDeleted=False)

class Topic(models.Model):
    name = models.CharField(max_length=255)

    isDeleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.DO_NOTHING,
        null = True,
        blank = True
    )

    history = models.ManyToManyField(History)
    objects = TopicManager()

    def update(self, oldValue, currentUser=None):
        self.history.create(
            action = History.Action.UPDATE,
            field = 'name',
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
