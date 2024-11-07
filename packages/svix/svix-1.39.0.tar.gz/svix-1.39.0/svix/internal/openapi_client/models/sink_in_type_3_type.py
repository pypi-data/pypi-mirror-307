from enum import Enum


class SinkInType3Type(str, Enum):
    HTTP = "http"

    def __str__(self) -> str:
        return str(self.value)
