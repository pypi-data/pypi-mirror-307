from typing import Dict, Any

class ErrorMessage:
    IMPLEMENTATION_ERROR = "Implementation error"
    MISMATCH_LAST_CURRENT_INDEX = "Mismatch last current index"
    MISSING_SEGMENT_ID = "Missing segment id"
    MISSING_FILE = "Missing file"

class BaseError(Exception):
    def __init__(self, message: str, data: Dict[Any, Any] = None):
        self.message = message
        self.data = data
