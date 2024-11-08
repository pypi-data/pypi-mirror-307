from decimal import Decimal
from typing import Any, List, Union

from yandex_b2b_go.errors import ValidationError


def error_string(field_name: str, value: Any, expected_type: str) -> str:
    return f'Invalid value for {field_name}: {value!r:.1024} is not instance of {expected_type}'


def serialize_integer(value: int, field_name: str) -> str:
    if not isinstance(value, int):
        raise ValidationError(error_string(field_name, value, 'int'))

    return str(value)


def serialize_list(value: List[str], field_name: str) -> str:
    if not isinstance(value, list):
        raise ValidationError(error_string(field_name, value, 'list of str'))

    return str(','.join(value))


def serialize_number(
    value: Union[float, int, Decimal],
    field_name: str,
) -> str:
    if not isinstance(value, (float, int, Decimal)):
        raise ValidationError(error_string(field_name, value, '(float, int, decimal.Decimal)'))
    if isinstance(value, int):
        return str(value)

    return str(float(value))
