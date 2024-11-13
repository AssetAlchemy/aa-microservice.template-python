import uuid
from config.envs import source


class MessageBase:
    def __init__(self, message_dict):
        print(message_dict)

        self.message_id = getattr(message_dict, "message_id", None)
        self.message_version = getattr(message_dict, "message_version", None)
        self.trace_id = getattr(message_dict, "trace_id", None)
        self.asset_id = getattr(message_dict, "asset_id", None)
        self.status = getattr(message_dict, "status", None)
        self.source = getattr(message_dict, "source", None)
        self.options = getattr(message_dict, "options", {})


class MessageRecieved(MessageBase):
    """Class to represent a received message."""

    def check_fields(self):
        """Validate that all required fields are present."""
        if not self.message_id:
            raise MissingFieldError("message_id")
        if not self.message_version:
            raise MissingFieldError("message_version")
        if not self.trace_id:
            raise MissingFieldError("trace_id")
        if not self.asset_id:
            print(self.asset_id)
            raise MissingFieldError("asset_id")
        if not self.status:
            raise MissingFieldError("status")
        if not self.source:
            raise MissingFieldError("source")

    def to_dict(self):
        return {
            "message_id": self.message_id,
            "message_version": self.message_version,
            "trace_id": self.trace_id,
            "asset_id": self.asset_id,
            "status": self.status,
            "source": self.source,
            "options": self.options,
        }


class MessageToSend(MessageBase):
    def __init__(self, message_dict):
        super().__init__(message_dict)
        self.message_id = str(uuid.uuid4())
        self.status = "normal"
        self.source = source
        self.check_fields()

    def check_fields(self):
        if not self.message_version:
            raise MissingFieldError("message_version")
        if not self.trace_id:
            raise MissingFieldError("trace_id")
        if not self.asset_id:
            raise MissingFieldError("asset_id")

    def to_dict(self):
        return {
            "message_id": self.message_id,
            "message_version": self.message_version,
            "trace_id": self.trace_id,
            "asset_id": self.asset_id,
            "status": self.status,
            "source": self.source,
            "options": self.options,
        }


class MessageErrorToSend(MessageBase):
    def __init__(self, message_dict):
        super().__init__(message_dict)
        self.message_id = str(uuid.uuid4())
        self.status = "error"
        self.error = getattr(message_dict, "error", None)
        self.source = source

    def to_dict(self):
        return {
            "message_id": self.message_id,
            "message_version": self.message_version,
            "trace_id": self.trace_id,
            "asset_id": self.asset_id,
            "status": self.status,
            "error": self.error,
            "source": self.source,
            "options": self.options,
        }


class MissingFieldError(Exception):
    """Custom exception it is raised when there is a required field."""

    def __init__(self, field_name):
        self.field_name = field_name
        super().__init__(f"The field '{self.field_name}' is required but missing.")
