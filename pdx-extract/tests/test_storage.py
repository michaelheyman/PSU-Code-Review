import unittest.mock as mock

from app import storage


@mock.patch("google.cloud.storage.Client")
def test_upload_to_bucket_returns_none_when_no_bucket(mock_storage_client):
    mock_created_bucket = mock.Mock()
    mock_created_bucket.name = "test-bucket"
    mock_storage_client().lookup_bucket.return_value = None
    mock_storage_client().create_bucket.return_value = mock_created_bucket
    contents = {}

    storage.upload_to_bucket(contents)

    assert mock_storage_client().lookup_bucket.called is True
    assert mock_storage_client().create_bucket.called is True


@mock.patch("app.storage.write_lambda_file")
@mock.patch("app.utils.generate_filename")
@mock.patch("google.cloud.storage.Client")
def test_upload_to_bucket_runs_until_end(
    mock_storage_client, mock_generate_filename, mock_write_lambda_file
):
    lookup_bucket = mock.Mock()
    lookup_bucket.name = "test-bucket"
    bucket_blob = mock.Mock()
    lookup_bucket.blob.return_value = bucket_blob
    mock_storage_client().lookup_bucket.return_value = lookup_bucket
    mock_generate_filename.return_value = "1234567890.json"
    contents = {}

    storage.upload_to_bucket(contents)

    assert mock_storage_client().lookup_bucket.called is True
    assert mock_storage_client().create_bucket.called is False


def test_write_lambda_file_returns_filename():
    filename = "test-filename"
    contents = "test-contents"

    with mock.patch(
        "builtins.open", new_callable=mock.mock_open()
    ) as mock_open:  # noqa: F841
        with mock.patch("json.dump") as mock_json:  # noqa: F841
            pass

    lambda_filename = storage.write_lambda_file(filename, contents)

    assert lambda_filename == "/tmp/test-filename"
