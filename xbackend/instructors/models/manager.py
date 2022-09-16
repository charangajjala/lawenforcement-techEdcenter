from django.db import models

class InstructorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(isDeleted = False)
