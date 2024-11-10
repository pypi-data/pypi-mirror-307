from typing import Union

from .. import errors
from .base import FieldType, FieldTypeABC


class String(FieldType, FieldTypeABC):
    def __init__(self, size: int) -> None:
        super().__init__(size)
        self._size = size

    def _validate_encode(self, text: str) -> None:
        if not isinstance(text, str):
            raise TypeError('`text` parameter must be a string')

        if len(text.encode(encoding='utf8')) > self._size:
            raise errors.str_value_oversized_error(self)

    def encode(self, text: str) -> bytes:
        self._validate_encode(text)
        return text.encode(encoding='utf8') + (
            (self._size - len(text)) * b'\0'
        )

    def _validate_decode(self, value: Union[bytes, bytearray]) -> None:
        if not isinstance(value, (bytes, bytearray)):
            raise TypeError(
                '`value` parameter must be of type bytes or bytearray'
            )

        if len(value) > self._size:
            raise errors.str_value_oversized_error(self)

    def decode(self, value: Union[bytes, bytearray], **kwargs: bool) -> str:
        self._validate_decode(value)

        string = ''
        for position, decimal in enumerate(value, 1):
            if decimal == 0:
                break

            string += chr(decimal)

            if not kwargs.get('no_limit_by_size') and position == self._size:
                break

        return string


Str = String
