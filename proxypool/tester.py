import time
import asyncio
import aiohttp
try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError
import sys
from proxypool.db import RedisClient

VALID_STATUS_CODES = [200]
TEST_URL = 'http://www.baidu.com'
BACTH_TEST_SIZE = 100


class Tester():
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode("utf-8")
                real_proxy = 'http://' + proxy
                print("testing:", proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)
                        print("the proxy is avaliable:", proxy)
                    else:
                        self.redis.decrease(proxy)
                        print("the request code is not valid:", proxy)
            except (ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError):
                self.redis.decrease(proxy)
                print("failed to request the proxy:", proxy)

    def run(self):
        print("test is run")
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            for i in range(0, len(proxies), BACTH_TEST_SIZE):
                test_proxies = proxies[i:i + BACTH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print("Tester error", e.args)
