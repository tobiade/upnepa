import asyncio
from websockets import connect

async def listen():
    async with connect("ws://localhost:8765") as websocket:
        while True:
            message = await websocket.recv()
            print(f"Received: {message}")

asyncio.run(listen())