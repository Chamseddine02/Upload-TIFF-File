from django.db import models
from django.utils import timezone

class ChunkUpload(models.Model):
    upload_id = models.CharField(max_length=255, unique=True)
    total_chunks = models.IntegerField()
    received_chunks = models.IntegerField(default=0)
    file_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class UploadedFile(models.Model):
    name = models.CharField(max_length=255)
    size = models.BigIntegerField()
    upload_date = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to='uploads/')
