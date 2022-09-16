from django.db import models

class HostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(isDeleted = False)
