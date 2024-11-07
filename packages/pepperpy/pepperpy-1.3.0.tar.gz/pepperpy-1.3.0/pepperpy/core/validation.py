import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)


@dataclass
class ValidationRule(Generic[T]):
    """Regra de validação"""

    validator: Callable[[T], bool]
    message: str
    code: Optional[str] = None

    def validate(self, value: T) -> Optional[str]:
        """Executa validação"""
        return None if self.validator(value) else self.message


class Validator(ABC, Generic[T_co]):
    """Interface base para validadores"""

    @abstractmethod
    def validate(self, value: T_co) -> List[str]:
        """Valida um valor"""
        pass


class SchemaValidator(Validator):
    """Validador baseado em schema"""

    def __init__(self, schema: Dict[str, List[ValidationRule[T_co]]]) -> None:
        self.schema = schema

    def validate(self, data: Dict[str, Any]) -> List[str]:
        errors = []
        for field, rules in self.schema.items():
            value = data.get(field)
            for rule in rules:
                if error := rule.validate(value):
                    errors.append(f"{field}: {error}")
        return errors


class ValidationBuilder:
    """Builder para criar regras de validação"""

    @staticmethod
    def required(message: str = "Field is required") -> ValidationRule:
        return ValidationRule(lambda x: x is not None and str(x).strip() != "", message, "REQUIRED")

    @staticmethod
    def min_length(min_len: int, message: Optional[str] = None) -> ValidationRule:
        return ValidationRule(
            lambda x: len(str(x)) >= min_len,
            message or f"Minimum length is {min_len}",
            "MIN_LENGTH",
        )

    @staticmethod
    def max_length(max_len: int, message: Optional[str] = None) -> ValidationRule:
        return ValidationRule(
            lambda x: len(str(x)) <= max_len,
            message or f"Maximum length is {max_len}",
            "MAX_LENGTH",
        )

    @staticmethod
    def pattern(regex: str, message: str) -> ValidationRule:
        return ValidationRule(lambda x: bool(re.match(regex, str(x))), message, "PATTERN")

    @staticmethod
    def email(message: str = "Invalid email format") -> ValidationRule:
        return ValidationBuilder.pattern(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", message
        )

    @staticmethod
    def custom(
        validator: Callable[[Any], bool], message: str, code: Optional[str] = None
    ) -> ValidationRule:
        return ValidationRule(validator, message, code)
