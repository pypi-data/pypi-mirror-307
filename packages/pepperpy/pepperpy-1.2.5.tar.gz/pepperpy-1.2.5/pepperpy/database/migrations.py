from pathlib import Path
from typing import Optional

from alembic import command
from alembic.config import Config


class MigrationManager:
    """Database migration manager"""

    def __init__(self, migrations_dir: Optional[Path] = None) -> None:
        self.migrations_dir = migrations_dir or Path("migrations")
        self._config = None

    def _init_config(self, database_url: str) -> None:
        """Initialize Alembic configuration"""
        self._config = Config()
        self._config.set_main_option("script_location", str(self.migrations_dir))
        self._config.set_main_option("sqlalchemy.url", database_url)

    async def create_migration(self, name: str) -> None:
        """Create new migration"""
        command.revision(self._config, autogenerate=True, message=name)

    async def upgrade(self, database_url: str, revision: str = "head") -> None:
        """Upgrade database to specified revision"""
        self._init_config(database_url)
        command.upgrade(self._config, revision)

    async def downgrade(self, database_url: str, revision: str) -> None:
        """Downgrade database to specified revision"""
        self._init_config(database_url)
        command.downgrade(self._config, revision)

    async def current(self, database_url: str) -> str:
        """Get current migration revision"""
        self._init_config(database_url)
        return command.current(self._config)
