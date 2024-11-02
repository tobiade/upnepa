import asyncio
import json
from math import pi
import redis.asyncio as redis
from websockets.asyncio.server import serve, broadcast
from redis.asyncio.client import PubSub
import sys
import aiohttp
from typing import Optional

from constants import LED_CHANNEL, LED_QUEUE


class ConnectionHandler:
    def __init__(self, redisURL: str, piURL: str):
        self.connections = set()
        self.r = redis.from_url(redisURL)
        self.session: Optional[aiohttp.ClientSession] = None  # Initialize session as None
        self.piURL = piURL

    async def start(self):
        """ Initialize the aiohttp ClientSession """
        self.session = aiohttp.ClientSession()

    async def close(self):
        """ Close the aiohttp ClientSession """
        if self.session:
            await self.session.close()

    def add_connection(self, websocket):
        self.connections.add(websocket)
    
    async def store(self, message: str):
        # Set the LEDs and publish the LED state to the Redis channel
        try:
            # post json to piURL
            # if self.session is None:
            #     raise RuntimeError("ClientSession is not initialized.")
            # async with self.session.post(self.piURL, data=message, headers={"Content-Type": "application/json"}) as response:
                # respBody = await response.text() # Use await to get the response body
            #     print("response:", respBody)
            await self.r.lpush(LED_QUEUE, message)
            # await self.r.publish(LED_CHANNEL, respBody)
            # print("published message:", respBody)
        except Exception as e:
            print(e)

    async def listen(self, websocket):
        async def reader(channel: PubSub):
            while True:
                try:
                    message = await channel.get_message(ignore_subscribe_messages=True)
                    if message is not None:
                        if message['type'] == 'message':
                            leds = message['data']
                            print("got message:", leds)
                            # broadcast(self.connections, leds.decode(), raise_exceptions=True)
                            await websocket.send(leds.decode())
                except Exception as e:
                    print(e)

        psub: PubSub = self.r.pubsub()
        async with psub as p:
            await p.subscribe(LED_CHANNEL)
            await reader(p)  # wait for reader to complete
            await p.unsubscribe(LED_CHANNEL)

        # closing all open connections
        await psub.close()


connection_handler = ConnectionHandler(redisURL='redis://localhost', piURL='http://localhost:5000/led')


async def display_leds(websocket):
    leds = {"leds": "****"}
    await websocket.send(json.dumps(leds))


async def handler(websocket):
    # connection_handler.add_connection(websocket)
    # await display_leds(websocket)

    asyncio.create_task(connection_handler.listen(websocket))


    async for message in websocket:
        await connection_handler.store(message)


async def main():
    # Initialize the aiohttp ClientSession
    await connection_handler.start()

    try:
        async with serve(handler, "0.0.0.0", int(sys.argv[1])):
            # asyncio.create_task(connection_handler.listen())
            await asyncio.get_running_loop().create_future()  # run forever
    finally:
        # Ensure the ClientSession is closed on shutdown
        await connection_handler.close()


asyncio.run(main())
