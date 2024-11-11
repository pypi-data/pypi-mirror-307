import asyncio
import socket
import signal


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = None

    async def start_server(self):
        self.server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f"Serving on {self.server.sockets[0].getsockname()}")
        async with self.server:
            await self.server.serve_forever()

    async def handle_client(self, reader, writer):
        # 处理客户端连接
        pass

    async def shutdown(self, signal=None):
        if signal:
            print(f"Received exit signal {signal.name}...")
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            print("Server shut down.")


async def main():
    # 创建服务器实例
    server = Server('127.0.0.1', 12345)

    # 创建一个任务来监听信号
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(server.shutdown(sig)))

    try:
        await server.start_server()
    except Exception as e:
        print(f"Unexpected exception: {e}")
    finally:
        loop.close()


if __name__ == '__main__':
    asyncio.run(main())
