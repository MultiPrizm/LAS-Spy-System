from django.db import models
import uuid
from authorization.models import WorkStation

class Worker(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gmail = models.EmailField(max_length=255)
    face_hash = models.CharField(max_length=1024)
    station = models.ForeignKey(WorkStation, on_delete = models.DO_NOTHING)
