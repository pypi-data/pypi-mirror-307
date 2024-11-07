# minio_utils/minio_helper.py
import re
from minio import Minio
from django.conf import settings

def get_signed_url(file_path, expiry_hours=1):
  try:
    # Initialize the MinIO client
    client = Minio(
      settings.MINIO_STORAGE_ENDPOINT,
      access_key=settings.MINIO_STORAGE_ACCESS_KEY,
      secret_key=settings.MINIO_STORAGE_SECRET_KEY,
      region='fr',
      secure=settings.MINIO_STORAGE_USE_HTTPS,
    )
    
    # Extract bucket name and object path from file_path
    match = re.match(r'^\/([^\/]+)\/(.+)$', file_path)
    if not match:
      raise ValueError("Invalid file path format. Expected format: '/bucket_name/object_path'")
    
    bucket_name, object_path = match.groups()
    
    # Calculate the expiry time in seconds
    expiry_seconds = expiry_hours * 3600
    
    # Generate the presigned URL
    signed_url = client.presigned_get_object(bucket_name, object_path, expires=expiry_seconds)
    return signed_url
  except Exception as e:
    print(f"Error generating signed URL: {e}")
    return None


# USAGE OF IMPORTED PACKAGE 
# from minio_utils.minio_helper import get_signed_url

# signed_url = get_signed_url('/clubs-media/myfile.jpg', 24)  # Generates a signed URL for 24 hours

# NB: ADDING THESE IN settings.py   IS REQUIRED. 
# # settings.py 
# MINIO_STORAGE_ENDPOINT = 'your-minio-endpoint'
# MINIO_STORAGE_ACCESS_KEY = 'your-access-key'
# MINIO_STORAGE_SECRET_KEY = 'your-secret-key'
# MINIO_STORAGE_USE_HTTPS = True  # or False
