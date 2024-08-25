# upload/serializers.py
from rest_framework import serializers
from .models import ChunkUpload, UploadedFile

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'name', 'size', 'upload_date', 'chunks_total', 'chunks_received']


class FileChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChunkUpload
        fields = ['id', 'file_upload', 'chunk_number', 'data']
