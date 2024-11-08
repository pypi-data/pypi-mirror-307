from enum import Enum
from typing import Any, Optional


class CaseInsensitiveEnum(str, Enum):
    @classmethod
    def _missing_(cls, value: Any) -> Optional[str]:
        if isinstance(value, str):
            value = value.lower()
            for member in cls:
                if member.lower() == value:
                    return member
        return None
