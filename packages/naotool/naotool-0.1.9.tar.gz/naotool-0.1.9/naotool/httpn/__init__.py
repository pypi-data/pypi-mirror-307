import asyncio
import time

from httpx import AsyncClient


class AutoCloseAsyncClient(AsyncClient):
    """
    1.自动关闭
    AutoCloseAsyncClient会在指定的超时（timeout）后自动关闭，如果在这段时间内没有调用任何方法。
    2.上下文管理
    使用异步上下文管理器（__aenter__和__aexit__），在使用完客户端后确保资源得到清理。
    """

    # 超时时间，默认为30s
    auto_close_time: int
    last_action_time = time.monotonic()
    _running = True

    def __init__(self, auto_close_time: int = 30, *args, **kwargs):
        self.auto_close_time = auto_close_time
        self._timeout_task = asyncio.create_task(self._check_timeout())
        kwargs["trust_env"] = False  # ban proxy
        super().__init__(*args, **kwargs)

    async def _check_timeout(self):
        while self._running:
            await asyncio.sleep(1)
            if time.monotonic() - self.last_action_time > self.auto_close_time:
                await self.close()

    async def _update_action_time(self):
        self.last_action_time = time.monotonic()

    async def get(self, *args, **kwargs):
        await self._update_action_time()
        return await super().get(*args, **kwargs)

    async def post(self, *args, **kwargs):
        await self._update_action_time()
        return await super().post(*args, **kwargs)

    async def close(self):
        self._running = False
        await super().aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()
        self._timeout_task.cancel()


# 使用示例
async def main():
    async with AsyncClient(trust_env=False) as client:
        print(await client.get("https://baidu.com"))  # 发起请求

    client = AutoCloseAsyncClient(auto_close_time=3)
    print(await client.get("https://baidu.com"))  # 发起请求

    await asyncio.sleep(1)  # 等待小于超时的时间

    print("Waiting for timeout...")
    await asyncio.sleep(3)  # 等待大于超时的时间
    print("Client should be closed now.")


# 运行示例
if __name__ == "__main__":
    asyncio.run(main())
