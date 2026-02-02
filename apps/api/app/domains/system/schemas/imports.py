from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, EmailStr, Field

class ImportRowStatus(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    WARNING = "WARNING"
    DUPLICATE = "DUPLICATE"

class ImportExecuteRequest(BaseModel):
    file_token: str
