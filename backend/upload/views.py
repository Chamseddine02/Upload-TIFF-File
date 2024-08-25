# backend/upload/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import ChunkUpload, UploadedFile
import os

@csrf_exempt
def receive_chunk(request):
    if request.method == 'POST':
        upload_id = request.POST.get('upload_id')
        chunk_index = int(request.POST.get('chunk_index'))
        total_chunks = int(request.POST.get('total_chunks'))
        file_name = request.POST.get('file_name')
        file_size = int(request.POST.get('file_size'))
        chunk_data = request.FILES.get('file')

        if not upload_id or not file_name or not chunk_data:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

      
        chunk_upload, created = ChunkUpload.objects.get_or_create(
            upload_id=upload_id,
            defaults={
                'file_name': file_name,
                'file_size': file_size,
                'total_chunks': total_chunks
            }
        )

        
        temp_dir = f"temp/{upload_id}"
        os.makedirs(temp_dir, exist_ok=True)
        
        chunk_file_path = os.path.join(temp_dir, f"chunk_{chunk_index}")
        with open(chunk_file_path, 'wb') as f:
            for chunk in chunk_data.chunks():
                f.write(chunk)

        # Update received chunks count
        chunk_upload.received_chunks += 1
        chunk_upload.save()

        return JsonResponse({'message': 'Chunk received successfully', 'received_chunks': chunk_upload.received_chunks})

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def combine_chunks(request):
    if request.method == 'POST':
        upload_id = request.POST.get('upload_id')
        chunk_upload = get_object_or_404(ChunkUpload, upload_id=upload_id)

        if chunk_upload.received_chunks == chunk_upload.total_chunks:
            final_file_path = f"uploads/{chunk_upload.file_name}"
            os.makedirs(os.path.dirname(final_file_path), exist_ok=True)
            
            with open(final_file_path, 'wb') as final_file:
                for i in range(chunk_upload.total_chunks):
                    chunk_file_path = f"temp/{upload_id}/chunk_{i}"
                    with open(chunk_file_path, 'rb') as chunk_file:
                        final_file.write(chunk_file.read())

            uploaded_file = UploadedFile.objects.create(
                name=chunk_upload.file_name,
                size=chunk_upload.file_size,
                file=final_file_path
            )

            for i in range(chunk_upload.total_chunks):
                os.remove(f"temp/{upload_id}/chunk_{i}")
            os.rmdir(f"temp/{upload_id}")

            chunk_upload.delete()
            return JsonResponse({'message': 'File uploaded successfully', 'file_id': uploaded_file.id})

        return JsonResponse({'error': 'Not all chunks have been received'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def list_uploaded_files(request):
    files = UploadedFile.objects.all().values('id', 'name', 'size', 'upload_date')
    return JsonResponse(list(files), safe=False)


@csrf_exempt
def delete_uploaded_file(request, file_id):
    if request.method == 'DELETE':
        uploaded_file = get_object_or_404(UploadedFile, id=file_id)
        uploaded_file.file.delete()  
        uploaded_file.delete() 
        return JsonResponse({'message': 'File deleted successfully'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)
