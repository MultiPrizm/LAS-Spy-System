from django.db import models
import uuid
from authorization.models import WorkStation
from django.core.validators import MinValueValidator
from django.utils.timezone import localdate

class Worker(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gmail = models.EmailField(max_length=255)
    face_image = models.ImageField(null=True, blank=True)
    face_hash = models.BinaryField()
    station = models.ForeignKey(WorkStation, on_delete = models.DO_NOTHING)
    work_time = models.IntegerField(null=True, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"Worker: {self.first_name} {self.last_name}"


class DailyWorkReport(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    date = models.DateField(default=localdate)
    start_time = models.TimeField()
    finish_time = models.TimeField()
    additional = models.TextField(max_length = 30000, null = True)
    common_work_time = models.TextField(max_length=255, null = True)
    common_break_time = models.TextField(max_length=255, null = True)
    work_efficiency = models.TextField(max_length=255, null = True)

class BrowserHistoryItem(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    date = models.DateField(default=localdate)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    profile = models.TextField(max_length=32)
    title = models.TextField(max_length=128)
    url = models.TextField(max_length=64)
    time = models.TextField(max_length=32, null=True)