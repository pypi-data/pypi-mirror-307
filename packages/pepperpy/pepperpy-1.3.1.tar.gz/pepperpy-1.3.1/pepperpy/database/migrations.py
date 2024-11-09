"""Database migration management"""

import logging
from typing import Any, Dict, List, Optional

from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy.ext.asyncio import AsyncEngine

from .exceptions import MigrationError


class MigrationManager:
    """Manages database migrations"""

    def __init__(self, engine: AsyncEngine, migrations_dir: Optional[str] = None):
        self._engine = engine
        self._migrations_dir = migrations_dir or "migrations"
        self._logger = logging.getLogger(__name__)
        self._config = self._create_alembic_config()

    async def run_migrations(self) -> None:
        """Run pending migrations"""
        try:
            # Get current and head versions
            current = await self._get_current_version()
            head = self._get_head_version()

            if current == head:
                self._logger.info("Database is up to date")
                return

            self._logger.info(f"Running migrations from {current} to {head}")
            await self._run_upgrade()

        except Exception as e:
            raise MigrationError(f"Migration failed: {e}") from e

    async def create_migration(self, message: str) -> None:
        """Create new migration revision"""
        try:
            command.revision(
                self._config,
                message=message,
                autogenerate=True,
            )
        except Exception as e:
            raise MigrationError(f"Failed to create migration: {e}") from e

    async def _get_current_version(self) -> str:
        """Get current database version"""
        async with self._engine.connect() as conn:
            context = MigrationContext.configure(conn)
            return context.get_current_revision() or "base"

    def _get_head_version(self) -> str:
        """Get latest migration version"""
        script = ScriptDirectory.from_config(self._config)
        return script.get_current_head() or "base"

    async def _run_upgrade(self) -> None:
        """Run database upgrade"""
        command.upgrade(self._config, "head")

    def _create_alembic_config(self) -> Config:
        """Create Alembic configuration"""
        config = Config()
        config.set_main_option("script_location", self._migrations_dir)
        config.set_main_option("sqlalchemy.url", str(self._engine.url))
        return config

    async def get_migration_history(self) -> List[Dict[str, Any]]:
        """Get migration history"""
        script = ScriptDirectory.from_config(self._config)
        history = []

        for revision in script.walk_revisions():
            history.append(
                {
                    "revision": revision.revision,
                    "down_revision": revision.down_revision,
                    "message": revision.doc,
                    "created": revision.module.created,
                }
            )

        return history
