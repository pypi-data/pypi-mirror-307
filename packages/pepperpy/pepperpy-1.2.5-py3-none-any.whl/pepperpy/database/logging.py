from typing import Any, Dict, Optional

from pepperpy.core.logging import get_logger


class DatabaseLogger:
    """Database specific logger with query formatting"""

    def __init__(self, name: str = "database") -> None:
        self._logger = get_logger(name)
        self._query_counter = 0

    def log_query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None,
        duration: Optional[float] = None,
        rows_affected: Optional[int] = None,
    ) -> None:
        """Log database query with formatting"""
        self._query_counter += 1

        # Format query for logging
        formatted_query = self._format_query(query, params)

        # Build log message
        msg = f"Query #{self._query_counter}: {formatted_query}"
        if duration is not None:
            msg += f" (duration: {duration:.2f}s)"
        if rows_affected is not None:
            msg += f" (rows affected: {rows_affected})"

        self._logger.debug(msg)

    def log_transaction(
        self,
        event: str,
        transaction_id: str,
        duration: Optional[float] = None,
        error: Optional[Exception] = None,
    ) -> None:
        """Log transaction events"""
        msg = f"Transaction {transaction_id}: {event}"
        if duration is not None:
            msg += f" (duration: {duration:.2f}s)"

        if error:
            self._logger.error(msg, exc_info=error)
        else:
            self._logger.info(msg)

    def _format_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> str:
        """Format query with parameters for logging"""
        if not params:
            return query.strip()

        formatted = query.strip()
        for key, value in params.items():
            placeholder = f":{key}"
            formatted = formatted.replace(
                placeholder, f"'{value}'" if isinstance(value, str) else str(value)
            )
        return formatted
