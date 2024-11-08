import pytest
from unittest.mock import MagicMock, patch
from happtiq_commons_google_cloud.gcs_api_service import GcsApiService

@pytest.fixture
def gcs_api_service(monkeypatch):
    monkeypatch.setattr("google.auth.default", MagicMock(return_value=(MagicMock(universe_domain="googleapis.com"),"some-proje")))
    return GcsApiService(timeout=30)

def mock_storage_client():
    mock_blob = MagicMock()
    mock_blob.download_as_text.return_value = "Downloaded text"
    mock_bucket = MagicMock()
    mock_bucket.blob.return_value = mock_blob
    mock_client = MagicMock()
    mock_client.bucket.return_value = mock_bucket    
    return mock_client

def test_download_as_text(gcs_api_service, monkeypatch):
    monkeypatch.setattr(gcs_api_service, "client", mock_storage_client())

    bucket_name = "test-bucket"
    source_blob_name = "test-file.txt"
    
    text = gcs_api_service.download_as_text(bucket_name, source_blob_name)
    assert text == "Downloaded text"
    gcs_api_service.client.bucket.assert_called_once_with(bucket_name)
    gcs_api_service.client.bucket().blob.assert_called_once_with(source_blob_name)

def test_upload(gcs_api_service, monkeypatch):
    mock_client = MagicMock()
    mock_client.bucket.return_value = MagicMock(blob=MagicMock(upload_from_string=MagicMock()))
    monkeypatch.setattr(gcs_api_service, "client", mock_client)

    fileContent = b"Test file content"
    bucket_name = "test-bucket"
    destination = "test-file.txt"
    content_type = "text/plain"

    result = gcs_api_service.upload(fileContent, bucket_name, destination, content_type)
    assert result == f"gs://{bucket_name}/{destination}"
    gcs_api_service.client.bucket.assert_called_once_with(bucket_name)
    gcs_api_service.client.bucket().blob.assert_called_once_with(destination)
    gcs_api_service.client.bucket().blob(destination).upload_from_string.assert_called_once_with(fileContent, content_type=content_type, timeout=30)

def test_upload_file(gcs_api_service, monkeypatch):
    mock_client = MagicMock()
    mock_client.bucket.return_value = MagicMock(blob=MagicMock(upload_from_filename=MagicMock()))
    monkeypatch.setattr(gcs_api_service, "client", mock_client)

    file_path = "test-file.txt"
    bucket_name = "test-bucket"
    destination = "test-file.txt"
    content_type = "text/plain"

    result = gcs_api_service.upload_file(file_path, bucket_name, destination, content_type)
    assert result == f"gs://{bucket_name}/{destination}"
    gcs_api_service.client.bucket.assert_called_once_with(bucket_name)
    gcs_api_service.client.bucket().blob.assert_called_once_with(destination)
    gcs_api_service.client.bucket().blob(destination).upload_from_filename.assert_called_once_with(file_path, content_type=content_type, timeout=30)

def test_upload_file_gzipped(gcs_api_service, monkeypatch):
    mock_client = MagicMock()
    mock_client.bucket.return_value = MagicMock(blob=MagicMock(upload_from_filename=MagicMock()))
    monkeypatch.setattr(gcs_api_service, "client", mock_client)

    file_path = "test-file.txt"
    bucket_name = "test-bucket"
    destination = "test-file.txt"
    content_type = "text/plain"

    result = gcs_api_service.upload_file(file_path, bucket_name, destination, content_type, gzipped=True)
    assert result == f"gs://{bucket_name}/{destination}"
    gcs_api_service.client.bucket.assert_called_once_with(bucket_name)
    gcs_api_service.client.bucket().blob.assert_called_once_with(destination)
    gcs_api_service.client.bucket().blob(destination).upload_from_filename.assert_called_once_with(file_path, content_type=content_type, timeout=30)
    gcs_api_service.client.bucket().blob(destination).content_encoding = "gzip"

def test_list_files_with_prefix(gcs_api_service, monkeypatch):
    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob1 = MagicMock()
    mock_blob1.name = "file1.txt"
    mock_blob2 = MagicMock()
    mock_blob2.name = "file2.txt"
    mock_blobs = [mock_blob1,mock_blob2]

    mock_client.bucket.return_value = mock_bucket
    mock_bucket.list_blobs.return_value = mock_blobs
    monkeypatch.setattr(gcs_api_service, "client", mock_client)

    bucket_name = "test-bucket"
    prefix = "test-prefix/"

    result = gcs_api_service.list_files_with_prefix(bucket_name, prefix)

    assert result == ["file1.txt", "file2.txt"]
    mock_client.bucket.assert_called_once_with(bucket_name)
    mock_bucket.list_blobs.assert_called_once_with(prefix=prefix)
