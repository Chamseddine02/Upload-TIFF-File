# backend/upload/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('upload_chunk/', views.receive_chunk, name='upload_chunk'),
    path('combine_chunks/', views.combine_chunks, name='combine_chunks'),
    path('files/', views.list_uploaded_files, name='list_uploaded_files'),
    path('delete_file/<int:file_id>/', views.delete_uploaded_file, name='delete_uploaded_file'),
]