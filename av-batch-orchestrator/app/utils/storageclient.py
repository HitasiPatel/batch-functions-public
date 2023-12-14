"""Blob Storage client.
"""
import os
from azure.storage.blob import BlobServiceClient


class StorageClient:
    """Blob Storage client"""

    blobServiceClient: BlobServiceClient
    client: any

    def __init__(self, storageAccountUrl: str, credentials: any, containerName: str) -> None:
        """Constructor used to create storage and blob client.

        Args:
            storageAccountUrl (str): Url of the storage account
            credentials (any): Credentials for connecting to storage account.
            containerName (str): Name of the container.
        """
        self.blobServiceClient = BlobServiceClient(
            account_url=storageAccountUrl, credential=credentials
        )
        self.client = self.blobServiceClient.get_container_client(container=containerName)


    def getFirstLevelListOfDirectoryNames(self, path) -> list:
        """Get list of directory names from the given path

        Args:
            path (_type_): Path from which you want to get list of directories.
            recursive (bool, optional): _description_. Defaults to False.

        Returns:
            list: List of directories.
        """

        if not path == "" and not path.endswith("/"):
            path += "/"

        blob_iter = self.client.walk_blobs(path, delimiter='/')
        dirset = set()
        for blob in blob_iter:
            if blob.name.endswith("/") :
                dirset.add(blob.name)
        return list(dirset)
