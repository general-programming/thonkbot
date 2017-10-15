from raven.transport import AsyncTransport
from aiohttp import ClientSession
from asyncio import get_event_loop

class AioHttpTransport(AsyncTransport):
    def async_send(self, url, data, headers, success_cb, error_cb):
        async def request():
            async with ClientSession() as session:
                res = await session.request("POST", url, headers=headers, data=data)

                if res.status == 200:
                    success_cb()
                else:
                    raise Exception(res.status)

        task = get_event_loop().create_task(request())

        def done(task):
            if task.exception() is not None:
                error_cb(task.exception())

        task.add_done_callback(done)
