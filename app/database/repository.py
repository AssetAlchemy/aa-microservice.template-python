from gridfs.errors import NoFile
from .connection import fs


def get_file(file_id):
    try:
        if file_id is None:
            return file_id
        return fs.get(file_id)
    except NoFile as e:
        raise FileNotFound(file_id) from e
    except Exception as e:
        raise GetFileError(file_id) from e


def upload_file(file_data):
    try:
        return fs.put(file_data.read(), filename=file_data.filename)
    except Exception as e:
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
        super().__init__(f"Error updaloading file")
