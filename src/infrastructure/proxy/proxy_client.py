import httpx
import ssl

from src.config.settings import Config

timeout = httpx.Timeout(60.0)

ssl_context = ssl.create_default_context()
ssl_context.options |= ssl.OP_NO_TLSv1


class AgentAuthClient(httpx.AsyncClient):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            base_url=Config.AUTH_URL,
            verify=False,
            timeout=timeout,
            **kwargs,
        )


class AgentProfileClient(httpx.AsyncClient):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            base_url=Config.PROFILE_URL,
            verify=False,
            timeout=timeout,
            **kwargs,
        )