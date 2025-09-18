import os
from google.cloud import storage
from fastapi import UploadFile

def get_bucket():
    """Initializes the GCS client and returns the bucket object."""
    GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME")
    if not GCS_BUCKET_NAME:
        # In a real application, you might want to raise an exception
        # or handle this case more gracefully.
        return None
    storage_client = storage.Client()
    return storage_client.bucket(GCS_BUCKET_NAME)

def upload_blob(file: UploadFile, destination_blob_name: str):
    """Uploads a file to the bucket."""
    bucket = get_bucket()
    if bucket is None:
        raise ConnectionError("GCS_BUCKET_NAME not set.")
    blob = bucket.blob(destination_blob_name)
    try:
        blob.upload_from_file(file.file, content_type=file.content_type)
    finally:
        file.file.close()
    return blob.public_url

def download_blob(source_blob_name: str):
    """Downloads a blob from the bucket."""
    bucket = get_bucket()
    if bucket is None:
        raise ConnectionError("GCS_BUCKET_NAME not set.")
    blob = bucket.blob(source_blob_name)
    return blob.download_as_bytes()

def list_blobs():
    """Lists all the blobs in the bucket."""
    bucket = get_bucket()
    if bucket is None:
        return []
    return [blob.name for blob in bucket.list_blobs()]

def delete_blob(blob_name: str):
    """Deletes a blob from the bucket."""
    bucket = get_bucket()
    if bucket is None:
        raise ConnectionError("GCS_BUCKET_NAME not set.")
    blob = bucket.blob(blob_name)
    blob.delete()
