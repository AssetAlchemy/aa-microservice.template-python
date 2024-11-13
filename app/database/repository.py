from .connection import fs


def get_file(file_id):
    try:
        return fs.get(file_id)
    except Exception as e:
        raise FileNotFound(file_id=file_id)


def upload_file(file_data):
    return fs.put(file_data.read(), filename=file_data.filename)


class FileNotFound(Exception):
    """Custom exception it is raised when there not exist file with an specific file_id."""

    def __init__(self, file_id):
        self.file_id = file_id
        super().__init__(f"File with file_id:'{self.file_id}' not found.")
