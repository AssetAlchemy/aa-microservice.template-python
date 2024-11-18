from gridfs.errors import NoFile
from bson.objectid import ObjectId

from .connection import fs, db


def get_file(file_id):
    try:
        file = fs.get(ObjectId(file_id))
        filemetadata = db.uploads.files.find_one({"_id": ObjectId(file_id)})
        return {"filedata": file, "filemetadata": filemetadata}
    except NoFile as e:
        print(e)
        raise FileNotFound(file_id) from e
    except Exception as e:
        print(e)
        raise GetFileError(file_id) from e


def upload_file(file):
    try:
        metadata = {
            "filename": file["filemetadata"]["filename"],
            "chunkSize": file["filemetadata"]["chunkSize"],
            "length": file["filemetadata"]["length"],
            "contentType": file["filemetadata"]["contentType"],
        }
        filedata = file["filedata"]
        return fs.put(filedata.read(), **metadata)
    except Exception as e:
        print(e)
        raise UploadFileError() from e


class FileNotFound(NoFile):
    """Custom exception it is raised when there not exist file with an specific file_id."""

    def __init__(self, file_id):
        self.file_id = file_id
        super().__init__(f"File with file_id: '{self.file_id}' not found.")


class GetFileError(Exception):
    """Custom exception it is raised when there is an error at getting file"""

    def __init__(self, file_id):
        self.file_id = file_id
        super().__init__(f"Error getting file with file_id: '{self.file_id}'")


class UploadFileError(Exception):
    """Custom exception it is raised when there is an error at updaloading file"""

    def __init__(self):
        super().__init__(f"Error uploading file")
