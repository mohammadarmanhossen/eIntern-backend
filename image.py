




import os
import boto3
import django
from django.core.wsgi import get_wsgi_application

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eIntern.settings')
application = get_wsgi_application()

# Model import (IMPORTANT)
from internship.models import Internship

# iDrive S3 client
s3 = boto3.client(
    's3',
    endpoint_url='https://s3.ap-southeast-1.idrivee2.com',
    aws_access_key_id='XfeW8yiaiWIcWGXa1eMY',
    aws_secret_access_key='vnB1I2SR09pa0p6uxGMc5vgqQPhBaCJa1BRR2czl'
)

BUCKET_NAME = 'django-upload-key'

# Upload loop
for internship in Internship.objects.all():
    if internship.image:
        local_path = internship.image.path

        if not os.path.exists(local_path):
            print(f"❌ File not found, skipping: {local_path}")
            continue

        file_name = os.path.basename(local_path)
        s3_key = f"uploads/{file_name}"

        s3.upload_file(
            local_path,
            BUCKET_NAME,
            s3_key,
            ExtraArgs={'ACL': 'public-read'}
        )

        internship.image.name = s3_key
        internship.save(update_fields=["image"])

        print(f"✅ Uploaded {file_name} -> {s3_key}")
