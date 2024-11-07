from pepperpy.core.validation import SchemaValidator, ValidationBuilder

# Database configuration validators
database_validators = {
    "backend": [
        ValidationBuilder.required("Backend is required"),
        ValidationBuilder.custom(
            lambda x: x in ["postgresql", "mysql", "sqlite", "duckdb"],
            "Invalid database backend",
        ),
    ],
    "connection.url": [
        ValidationBuilder.required("Database URL is required"),
        ValidationBuilder.pattern(r"^[a-zA-Z]+://.*$", "Invalid database URL format"),
    ],
    "pool.size": [
        ValidationBuilder.custom(
            lambda x: isinstance(x, int) and x > 0,
            "Pool size must be a positive integer",
        )
    ],
    "retry.max_attempts": [
        ValidationBuilder.custom(
            lambda x: isinstance(x, int) and x > 0,
            "Max retry attempts must be a positive integer",
        )
    ],
}

database_validator = SchemaValidator(database_validators)
