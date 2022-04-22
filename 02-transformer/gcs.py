
from google.cloud import storage

class MyGCS:

    def __init__(self, bucket_name: str) -> None:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        self.bucket = bucket

    def upload_blob(self, source_file_name: str, destination_blob_name: str) -> None:

        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)

        print(
            "File {} uploaded to {}.".format(
                source_file_name, destination_blob_name
            )
        )

    def download_blob(self, bucket_name: str, source_blob_name: str, destination_file_name: str) -> None:
        
        blob = self.bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)

        print(
            "Downloaded storage object {} from bucket {} to local file {}.".format(
                source_blob_name, bucket_name, destination_file_name
            )
        )
