"""Module for working with Google Drive API."""
import json
import logging

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from retry import retry

from ..goole_api.account import Account
from ..goole_api.goolge_services import GoogleServices
from ..logger import logger


class MimeTypes:
    """Mime Types class."""

    SPREADSHEET = "application/vnd.google-apps.spreadsheet"
    FOLDER = "application/vnd.google-apps.folder"
    JSON = "application/json"


class GoogleDriveService(GoogleServices):
    """Google Drive Service class."""

    def __init__(self, account: Account):
        """Initialize the Google Drive Service."""
        self.service = build("drive", "v3", credentials=self._get_credentials(account), cache_discovery=False)

    def create_folder_if_not_exists(self, folder_name: str) -> dict:
        """Create the folder if not exists."""
        root_folder = self.get_root_folder("QA - Run Reports")
        try:
            folder = self.get_child_folder_by_name(root_folder, folder_name)
            logger.info(f"Folder {folder_name} already exists")
            return folder
        except ValueError:
            folder = self.create_folder(folder_name=folder_name, parent=[root_folder])
            logger.info(f"Folder {folder_name} created")
            return folder

    def update_json_file(self, file: dict, data: dict) -> dict:
        """Update the JSON file."""
        with open("updated_file.json", "w") as temp_file:
            json.dump(data, temp_file)
        media = MediaFileUpload("updated_file.json", mimetype="application/json")
        self.service.files().update(fileId=file["id"], media_body=media).execute()
        return file

    def create_file_if_not_exists(self, folder: dict, file_name: str, mime_type=MimeTypes.SPREADSHEET) -> dict:
        """Create the file if not exists."""
        try:
            file = self.get_file_in_folder(folder, file_name, mime_type)
            logger.info(f"File {file['name']} already exists")
            return file
        except ValueError:
            file = self.create_file(file_name=file_name, folder=folder, mime_type=mime_type)
            logger.info(f"File {file['name']} created")
            return file

    def get_file_in_folder(self, parents: dict, file_name: str, mime_type: str) -> dict:
        """Get the Google Sheet in the folder."""
        query = f"'{parents['id']}' in parents and mimeType='{mime_type}'"
        files = self.__execute_get_query(query, ["id", "name"])
        for file in files:
            if file["name"] == file_name:
                return file
        else:
            raise ValueError(f"File {file_name} not found")

    def get_root_folder(self, path_name: str) -> dict:
        """Get the root folder."""
        folders = self.__execute_get_query(f"mimeType='{MimeTypes.FOLDER}'", ["id", "name"])
        for folder in folders:
            if folder["name"] == path_name:
                return folder

    def get_child_folder_by_name(self, root_folder: dict, folder_name: str) -> dict:
        """Get the child folder by name."""
        folders = self.__execute_get_query(
            f"mimeType='{MimeTypes.FOLDER}'  and '{root_folder['id']}' in parents", ["id", "name"]
        )
        for folder in folders:
            if folder["name"] == folder_name:
                return folder
        else:
            raise ValueError(f"Folder {folder_name} not found")

    def create_folder(self, folder_name: str, parent: list[dict]) -> dict:
        """Create the folder."""
        return self.__execute_create_query(file_name=folder_name, mime_type=MimeTypes.FOLDER, folders=parent)

    def create_file(self, file_name, folder, mime_type) -> dict:
        """Create the file."""
        return self.__execute_create_query(file_name=file_name, mime_type=mime_type, folders=[folder])

    @retry(tries=3, delay=1, exceptions=HttpError)
    def __execute_create_query(self, file_name: str, mime_type: str, folders: list[dict]) -> dict:
        try:
            file_metadata = {"name": file_name, "mimeType": mime_type}
            if folders:
                file_metadata["parents"] = [folder["id"] for folder in folders]
            return self.service.files().create(body=file_metadata).execute()
        except HttpError as error:
            logging.error(f"An error occurred during query execution: {error}")
            raise error

    @retry(tries=3, delay=1, exceptions=HttpError)
    def __execute_get_query(self, query: str, fields: list) -> list[dict]:
        files = []
        page_token = None
        while True:
            try:
                response = (
                    self.service.files()
                    .list(
                        q=query,
                        spaces="drive",
                        fields=f"nextPageToken, files({', '.join(fields)})",
                        pageToken=page_token,
                    )
                    .execute()
                )
                files.extend(response.get("files", []))
                page_token = response.get("nextPageToken")
                if not page_token:
                    break
            except HttpError as error:
                logging.error(f"An error occurred during query execution: {error}")
                raise error
        return files

    def lock_file(self, file: dict):
        """Lock the file."""
        self.service.files().update(fileId=file["id"], body={"appProperties": {"locked": "true"}}).execute()

    def unlock_file(self, file: dict):
        """Unlock the file."""
        self.service.files().update(fileId=file["id"], body={"appProperties": {"locked": "false"}}).execute()

    def check_file_locked(self, file: dict) -> bool:
        """Check if the file is locked."""
        file = self.service.files().get(fileId=file["id"], fields="appProperties").execute()
        locked = file.get("appProperties", {}).get("locked", "false")
        return locked == "true"

    @retry(tries=3, exceptions=ValueError)
    def get_file_content(self, file: dict) -> dict:
        """Get the file content."""
        file_content = self.service.files().get_media(fileId=file["id"]).execute()
        self.lock_file(file)
        if file_content:
            return json.loads(file_content.decode("utf-8"))
        else:
            return {}
