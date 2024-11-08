from google.cloud import storage
import logging

class GcsApiService:
    def __init__(self, timeout):
        self.client = storage.Client()
        self.logger = logging.getLogger(__name__)
        self.timeout = timeout


    def download_as_text(self, bucket_name: str, source_blob_name: str) -> str:
        self.logger.info(f"Downloading {bucket_name}/{source_blob_name}")
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        
        try:
            text = blob.download_as_text()
            self.logger.info(f"Downloaded {len(text)} chars from {bucket_name}/{source_blob_name}")
        except Exception as e:
            self.logger.error(f"Failed to download file {bucket_name}/{source_blob_name}: {e}")
            raise e
        
        return text
    
    def upload(self, fileContent: bytes,  bucket_name: str, destination: str, content_type: str) -> str:
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(destination)
        blob.upload_from_string(fileContent, content_type=content_type, timeout=self.timeout)
        self.logger.info(f"File uploaded to {destination}.")
        return f"gs://{bucket_name}/{destination}"
    
    def upload_file(self, file_path: bytes,  bucket_name: str, destination: str, content_type: str, gzipped = False) -> str:
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(destination)
        if gzipped:
            blob.content_encoding = "gzip"
        blob.upload_from_filename(file_path, content_type=content_type, timeout=self.timeout)
        self.logger.info(f"File uploaded to {destination}.")
        return f"gs://{bucket_name}/{destination}"
    
    def list_files_with_prefix(self, bucket_name: str, prefix: str):
        self.logger.info(f"Listing files in bucket {bucket_name} with prefix {prefix}")
        bucket = self.client.bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)

        file_list = [blob.name for blob in blobs]
        self.logger.debug(f"Files in bucket {bucket_name} with prefix {prefix}: {file_list}")
        self.logger.info(f"found {len(file_list)} files in bucket {bucket_name} with prefix {prefix}")
    
        return file_list
