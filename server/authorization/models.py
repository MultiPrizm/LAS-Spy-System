from django.db import models
import uuid

class WorkStation(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=256, null=True)

    def __str__(self):
        return "Work station: " + self.name

class AuthToken(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    description = models.CharField(max_length=256, null=True)
    jwt = models.CharField(max_length=256, default="")
    station = models.ForeignKey(WorkStation, on_delete = models.DO_NOTHING)
    active = models.BooleanField(default=1)
