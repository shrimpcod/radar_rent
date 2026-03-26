from curl_cffi.requests import AsyncSession
from parsers.utils.proxy import ProxyManager, load_proxies_from_env

_proxy_manager = ProxyManager(load_proxies_from_env())

async def make_session(proxy: str | None = None) -> AsyncSession:
    """
    Создаёт HTTP сессию с имитацией браузера Chrome.
    Если proxy не передан — берёт следующий из пула автоматически.
    """
    if proxy is None:
        proxy = _proxy_manager.get_proxy()

    return AsyncSession(
        impersonate="chrome120",
        proxy=proxy,
        timeout=30
    )