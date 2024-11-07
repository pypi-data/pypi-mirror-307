MinIO Helper for Digital Club

MinIO Helper is a specialized Python package developed for the Digital Club. This package facilitates the secure and time-limited access to files stored in a MinIO bucket by generating signed URLs.
Features

    Project-specific: Designed specifically for the Digital Club project, making integration seamless.
    Secure Access: Easily generate signed URLs to securely access objects stored in a MinIO bucket.
    Customizable Expiration: Set expiration time as needed for each URL.

Installation

To install MinIO Helper, first clone this repository and build the package:

bash

python setup.py sdist bdist_wheelv

Then, install the package locally:

bash

pip install dist/minio_helper-0.1-py3-none-any.whl

Or, if you prefer, use twine to upload to PyPI and install directly:

bash

twine upload dist/*
pip install minio_helper

Usage
1. Add MinIO Helper Configuration to settings.py

To configure MinIO Helper in your Django project, add the following settings to settings.py:

python

# settings.py
MINIO_STORAGE_ENDPOINT = 'your-minio-endpoint'
MINIO_STORAGE_ACCESS_KEY = 'your-access-key'
MINIO_STORAGE_SECRET_KEY = 'your-secret-key'
MINIO_STORAGE_USE_HTTPS = True  # Set to False if using HTTP

2. Using get_signed_url in Your Project

After setting up, you can use get_signed_url to create secure, temporary URLs for accessing files:

python

from minio_utils.minio_helper import get_signed_url

# Generate a signed URL with 24-hour expiration
signed_url = get_signed_url('/clubs-media/myfile.jpg', expiry_hours=24)
print(signed_url)

Example Usage in a Django View

python

from django.http import JsonResponse
from minio_utils.minio_helper import get_signed_url

def get_file_url(request, file_path):
    signed_url = get_signed_url(file_path, expiry_hours=24)
    return JsonResponse({'signed_url': signed_url})

Requirements

    Django
    MinIO Python SDK

License

This project is licensed under the MIT License. See the LICENSE file for details.
About Digital Club Project

This package was created for the Digital Club to ensure secure access to media assets stored in MinIO. The project aims to streamline file sharing and secure access for club members, partners, and stakeholders.
Contact

For questions or additional support, please contact the Digital Club.