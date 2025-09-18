import os
from google.cloud import storage
from fastapi import UploadFile

GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME")

def get_storage_client():
    return storage.Client()

def get_bucket():
    storage_client = get_storage_client()
    return storage_client.bucket(GCS_BUCKET_NAME)

def file_exists(filename: str) -> bool:
    """
    Checks if a file exists in the GCS bucket.
    """
    bucket = get_bucket()
    blob = bucket.blob(filename)
    return blob.exists()

def upload_file(file: UploadFile):
    """
    Uploads a file to the GCS bucket.
    """
    bucket = get_bucket()
    blob = bucket.blob(file.filename)
    blob.upload_from_file(file.file)

def list_files():
    """
    Lists all files in the GCS bucket.
    """
    storage_client = get_storage_client()
    blobs = storage_client.list_blobs(GCS_BUCKET_NAME)
    return [blob.name for blob in blobs]

def download_file(filename: str):
    """
    Downloads a file from the GCS bucket.
    """
    bucket = get_bucket()
    blob = bucket.blob(filename)
    return blob.download_as_bytes()

def delete_file(filename: str):
    """
    Deletes a file from the GCS bucket.
    """
    bucket = get_bucket()
    blob = bucket.blob(filename)
    blob.delete()
