from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

from .meta import Agenda
from .managers import CourseManager
from .topic import Topic
from meta.models import File, History

class Course(models.Model):
    courseNum = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    subTitle = models.CharField(max_length=255, null=True, blank=True)
    shortDesc = models.CharField(max_length=255, null=True, blank=True)
    description = ArrayField(models.CharField(max_length=511), null=True, blank=True)

    days = models.PositiveIntegerField(null=True)
    targetAudience = models.CharField(max_length=255, null=True, blank=True)
    prerequisites = models.CharField(max_length=255, null=True, blank=True)

    agenda = models.ManyToManyField(Agenda)
    topic = models.ManyToManyField(Topic)
    material = models.ManyToManyField(File)

    isNew = models.BooleanField(default=True)
    isActive = models.BooleanField(default=False)
    isDeleted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        null = True,
        blank = True
    )
    history = models.ManyToManyField(History)

    objects = CourseManager()

    def toDict(self):
        return dict(
            id = self.id,
            courseNum = self.courseNum,
            title = self.title,
            subTitle = self.subTitle,
            shortDesc = self.shortDesc,
            description = self.description,
            days = self.days,
            targetAudience = self.targetAudience,
            prerequisites = self.prerequisites,
            isNew = self.isNew,
            topic = [t.toDict() for t in self.topic.all()],
            agenda = [a.toDict() for a in self.agenda.all().order_by('day')],
        )

    def toAdminDict(self):
        return dict(
            self.toDict(),
            material = [m.toDict() for m in self.material.all()],
            isActive = self.isActive,
            created = self.created,
            createdBy = dict(
                id = self.createdBy.id,
                firstName = self.createdBy.firstName,
                lastName = self.createdBy.lastName
            ) if self.createdBy else None,
            history = [h.toDict() for h in self.history.all()],
        )

    def save(self, *args, **kwargs):
        print("<---- courses.models.Course.save ---->")
        super().save(*args, **kwargs)

    def update(self, oldValues, currentUser=None):
        print("<---- courses.models.Course.update ---->")

        for (field, oldValue) in oldValues.items():
            self.history.create(
                action = History.Action.UPDATE,
                field = field,
                oldValue = oldValue,
                createdBy = currentUser,
            )
        super().save()

    def delete(self, currentUser=None):
        print("<---- courses.models.Course.delete ---->")

        self.isDeleted = True
        self.history.create(
            action = History.Action.DELETE,
            createdBy = currentUser,
        )
        super().save()

    def clean(self):
        self.days = int(self.days)

    def __str__(self):
        return self.title
