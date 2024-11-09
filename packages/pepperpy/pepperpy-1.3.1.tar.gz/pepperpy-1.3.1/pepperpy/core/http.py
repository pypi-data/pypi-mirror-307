import os
from typing import Any, Dict, Optional, Union

import aiohttp
from aiohttp import ClientTimeout
from yarl import URL


class HTTPClient:
    """HTTP client with proxy support and common functionality"""

    def __init__(
        self,
        base_url: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Union[int, float] = 30,
        verify_ssl: bool = True,
    ):
        self.base_url = base_url
        self.default_headers = headers or {}
        self.timeout = ClientTimeout(total=timeout)
        self.verify_ssl = verify_ssl
        self._session: Optional[aiohttp.ClientSession] = None

    @staticmethod
    def _get_proxy_settings() -> Dict[str, str]:
        """Get proxy settings from environment variables"""
        proxy_settings = {}

        http_proxy = os.environ.get("HTTP_PROXY")
        https_proxy = os.environ.get("HTTPS_PROXY")

        if http_proxy:
            proxy_settings["http"] = http_proxy
        if https_proxy:
            proxy_settings["https"] = https_proxy

        return proxy_settings

    async def _ensure_session(self) -> aiohttp.ClientSession:
        """Ensure we have an active session"""
        if self._session is None or self._session.closed:
            # Configure proxy if environment variables are set
            proxy_settings = self._get_proxy_settings()

            self._session = aiohttp.ClientSession(
                base_url=self.base_url,
                headers=self.default_headers,
                timeout=self.timeout,
                trust_env=True,  # Allow environment proxy settings
                proxy=proxy_settings if proxy_settings else None,
            )
        return self._session

    def _build_url(self, path: str) -> str:
        """Build complete URL from path"""
        if self.base_url:
            return str(URL(self.base_url) / path.lstrip("/"))
        return path

    async def request(
        self,
        method: str,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> aiohttp.ClientResponse:
        """Make HTTP request with proxy support"""
        session = await self._ensure_session()

        # Merge headers
        request_headers = {**self.default_headers}
        if headers:
            request_headers.update(headers)

        url = self._build_url(path)

        try:
            response = await session.request(
                method, url, headers=request_headers, ssl=self.verify_ssl, **kwargs
            )
            return response
        except Exception as e:
            # Ensure session is closed on error
            await self.close()
            raise e

    async def get(self, path: str, **kwargs: Any) -> aiohttp.ClientResponse:
        """Make GET request"""
        return await self.request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs: Any) -> aiohttp.ClientResponse:
        """Make POST request"""
        return await self.request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs: Any) -> aiohttp.ClientResponse:
        """Make PUT request"""
        return await self.request("PUT", path, **kwargs)

    async def delete(self, path: str, **kwargs: Any) -> aiohttp.ClientResponse:
        """Make DELETE request"""
        return await self.request("DELETE", path, **kwargs)

    async def close(self) -> None:
        """Close client session"""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None
