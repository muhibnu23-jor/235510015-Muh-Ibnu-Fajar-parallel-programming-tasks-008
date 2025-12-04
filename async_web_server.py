from aiohttp import web
from dask.distributed import Client
import asyncio
def heavy_computation(x):
    import time
    time.sleep(2)
    return x * x

async def handle(request):
    n = int(request.query.get('n', '2'))
    future = client.submit(heavy_computation, n)
    result = await asyncio.wrap_future(future) 
    return web.Response(text=f"Result: {result}")

async def init_app():
    app = web.Application()
    app.router.add_get('/', handle)
    return app

if __name__ == "__main__":
    client = Client()
    print("Dask Cluster running…", client)
    app = asyncio.run(init_app())
    web.run_app(app, port=8080)
