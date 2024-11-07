from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from pepperpy.core.types import Status


@dataclass
class HealthStatus:
    """Health status information for a module"""

    module: str
    state: Status
    details: Dict[str, Any]


class HealthCheck:
    """Health check implementation for modules"""

    def __init__(self, module_name: str) -> None:
        self.module_name = module_name
        self.last_check: Optional[datetime] = None
        self.last_status: Optional[HealthStatus] = None

    async def check(self) -> HealthStatus:
        """Perform health check"""
        self.last_check = datetime.now()
        return HealthStatus(
            module=self.module_name, state=Status.ACTIVE, details={"last_check": self.last_check}
        )


class HealthMonitor:
    """Monitor health status of multiple modules"""

    def __init__(self) -> None:
        self._checks: Dict[str, HealthCheck] = {}

    def register(self, module_name: str) -> None:
        """Register a module for health monitoring"""
        self._checks[module_name] = HealthCheck(module_name)

    async def check_all(self) -> List[HealthStatus]:
        """Check health of all registered modules"""
        results = []
        for check in self._checks.values():
            results.append(await check.check())
        return results

    async def check_module(self, module_name: str) -> Optional[HealthStatus]:
        """Check health of a specific module"""
        if module_name in self._checks:
            return await self._checks[module_name].check()
        return None
