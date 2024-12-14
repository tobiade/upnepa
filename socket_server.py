import asyncio
import os
import ssl
import redis.asyncio as redis
from websockets.asyncio.server import serve
from redis.asyncio.client import PubSub
import sys

from constants import LED_CHANNEL, LED_QUEUE

CERT_PATH = '/etc/letsencrypt/live/upnepa.live/fullchain.pem'
KEY_PATH = '/etc/letsencrypt/live/upnepa.live/privkey.pem'

class ConnectionHandler:
    def __init__(self, redisURL: str):
        self.r = redis.from_url(redisURL)
    
    async def store(self, message: str):
        # Set the LEDs and publish the LED state to the Redis queue
        try:
            print("set LED state:", message)
            await self.r.lpush(LED_QUEUE, message)
        except Exception as e:
            print(e)

    async def listen(self, websocket):
        async def reader(channel: PubSub):
            try:
                async for message in channel.listen():
                    if message is not None:
                        if message['type'] == 'message':
                            leds = message['data']
                            print("got LED state:", leds)
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


connection_handler = ConnectionHandler(redisURL='redis://localhost')


async def handler(websocket):
    asyncio.create_task(connection_handler.listen(websocket))


    async for message in websocket:
        await connection_handler.store(message)

def ssl_cert_and_key_exist():
    return os.path.exists(CERT_PATH) and os.path.exists(KEY_PATH)

async def main():
    # Set up SSL if needed
    ssl_context = None
    if ssl_cert_and_key_exist():
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(CERT_PATH, keyfile=KEY_PATH)
        print("SSL context loaded")

    try:
        async with serve(handler, "0.0.0.0", int(sys.argv[1]), ssl=ssl_context):
            print("Server started")
            await asyncio.get_running_loop().create_future()  # run forever
    finally:
        print("Server stopped")


asyncio.run(main())
