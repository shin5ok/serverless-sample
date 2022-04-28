
from google.cloud import storage

class MyGCS:

    def __init__(self, bucket_name: str) -> None:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        self.bucket_name = bucket_name
        self.bucket = bucket

    def upload_blob(self, source_file_name: str, destination_blob_name: str) -> None:

        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)

        print(
            "File {} uploaded to {}.".format(
                source_file_name, destination_blob_name
            )
        )

    def download_blob(self, source_blob_name: str, destination_file_name: str) -> None:
        
        blob = self.bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)

        print(
            "Downloaded storage object {} from bucket {} to local file {}.".format(
                source_blob_name, self.bucket_name, destination_file_name
            )
        )

if __name__ == '__main__':
    import sys
    import uuid
    import pathlib
    cs = MyGCS(sys.argv[1])
    tmp = str(uuid.uuid4())
    cs.upload_blob("/etc/services", tmp)
    cs.download_blob(tmp, tmp)
    pathlib.Path(tmp).unlink()
