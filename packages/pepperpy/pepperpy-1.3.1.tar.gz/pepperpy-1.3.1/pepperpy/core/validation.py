"""Core validation system with common validators and rules"""

import re
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Type

from .exceptions import ValidationError


@dataclass
class ValidationRule:
    """Validation rule definition"""

    validator: Callable[[Any], bool]
    message: str
    params: Dict[str, Any] = None


class Validator:
    """Base validator class"""

    def __init__(self):
        self._rules: Dict[str, List[ValidationRule]] = {}

    def add_rule(self, field: str, rule: ValidationRule) -> None:
        """Add validation rule for field"""
        if field not in self._rules:
            self._rules[field] = []
        self._rules[field].append(rule)

    def validate(self, data: Dict[str, Any]) -> None:
        """Validate data against rules"""
        errors = []

        for field, rules in self._rules.items():
            value = data.get(field)
            for rule in rules:
                if not rule.validator(value):
                    errors.append(f"{field}: {rule.message}")

        if errors:
            raise ValidationError("\n".join(errors))


# Common validators
def required(value: Any) -> bool:
    """Check if value is not None"""
    return value is not None


def min_length(min_len: int) -> Callable[[Any], bool]:
    """Check minimum length"""
    return lambda value: len(value) >= min_len if value is not None else True


def max_length(max_len: int) -> Callable[[Any], bool]:
    """Check maximum length"""
    return lambda value: len(value) <= max_len if value is not None else True


def pattern(regex: str) -> Callable[[str], bool]:
    """Check if value matches regex pattern"""
    compiled = re.compile(regex)
    return lambda value: bool(compiled.match(value)) if value is not None else True


def range_check(
    min_val: Optional[float] = None, max_val: Optional[float] = None
) -> Callable[[float], bool]:
    """Check if value is within range"""

    def validator(value: float) -> bool:
        if value is None:
            return True
        if min_val is not None and value < min_val:
            return False
        if max_val is not None and value > max_val:
            return False
        return True

    return validator


def type_check(expected_type: Type) -> Callable[[Any], bool]:
    """Check value type"""
    return lambda value: isinstance(value, expected_type) if value is not None else True


def enum_check(valid_values: List[Any]) -> Callable[[Any], bool]:
    """Check if value is in enumeration"""
    return lambda value: value in valid_values if value is not None else True
