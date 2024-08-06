from google.cloud import storage

from app_server.config import BUCKET_NAME, BLOB_JSON


class BlobStorage:
    def __init__(self):
        from app import app

        app.logger.info("In BlobStorage")
        self.storage_client = storage.Client.from_service_account_json(BLOB_JSON)
        self.bucket = self.storage_client.bucket(BUCKET_NAME)
        app.logger.info("In BlobStorage initiated")

    def upload_blob(self, source_file_name):
        from app import app

        app.logger.info(f"In upload_blob {source_file_name = }")
        target_filename = source_file_name.split("/")[-1]
        blob = self.bucket.blob(source_file_name.split("/")[-1])
        response = blob.upload_from_filename(source_file_name)

        app.logger.info(f"{response =  }")

        file_url = blob.public_url
        gcs_uri = f"gs://{BUCKET_NAME}/{target_filename}"

        app.logger.info(f"File {source_file_name} uploaded. URL: {file_url}")
        return file_url, gcs_uri
