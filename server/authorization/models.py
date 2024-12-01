from django.db import models
import uuid

class WorkStation(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length=255)

class AuthToken(models.Model):
    token = models.CharField(max_length=16)
    station = models.ForeignKey(WorkStation, on_delete = models.DO_NOTHING)
