from typing import Dict, Any, Optional

from filum_utils.clients.notification import ErrorType

class ErrorMessage:
    IMPLEMENTATION_ERROR = "Implementation error"
    MISMATCH_LAST_CURRENT_INDEX = "Mismatch last current index"
    MISSING_SEGMENT_ID = "Missing segment id"
    MISSING_FILE = "Missing file"
    INVALID_DATETIME_STRING = "Invalid datetime string format - unable to parse"
    TIMEZONE_ERROR = "Timezone error"

class BaseError(Exception):
    def __init__(
        self,
        message: str,
        data: Optional[Dict[str, Any]] = None,
        error_code: Optional[int] = None,
        error_type: str = ErrorType.INTERNAL
    ):
        self.message = message
        self.data = data
        self.error_code = error_code
        self.error_type = error_type
