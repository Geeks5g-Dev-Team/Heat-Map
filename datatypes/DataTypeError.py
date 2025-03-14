from dataclasses import dataclass
from typing import Optional


@dataclass
class CustomError ():

    message: Optional[str]
    details: Optional[str]
    has_error: bool
