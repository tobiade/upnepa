import asyncio
import json
from math import pi
import os
import ssl
import redis.asyncio as redis
from websockets.asyncio.server import serve
from redis.asyncio.client import PubSub
import sys
import aiohttp
from typing import Optional

from constants import LED_CHANNEL, LED_QUEUE, LED_STREAM_CHANNEL
import io
import logging
import socketserver
from http import server
from threading import Condition

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

CERT_PATH = '/etc/letsencrypt/live/upnepa.live/fullchain.pem'
KEY_PATH = '/etc/letsencrypt/live/upnepa.live/privkey.pem'

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

class ConnectionHandler:
    def __init__(self, redisURL: str, piURL: str):
        self.connections = set()
        self.r = redis.from_url(redisURL)
        self.piURL = piURL

    async def start(self):
        """ Initialize the aiohttp ClientSession """
        self.session = aiohttp.ClientSession()

    async def close(self):
        """ Close the aiohttp ClientSession """
        if self.session:
            await self.session.close()


    
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
                            frame = message['data']
                            await websocket.send(frame)
                            # print("sent frame")
                except Exception as e:
                    print(e)

        psub: PubSub = self.r.pubsub()
        async with psub as p:
            await p.subscribe(LED_STREAM_CHANNEL)
            await reader(p)  # wait for reader to complete
            await p.unsubscribe(LED_STREAM_CHANNEL)

        # closing all open connections
        await psub.close()


connection_handler = ConnectionHandler(redisURL='redis://159.65.93.235', piURL='http://localhost:5000/led')

# picam2 = Picamera2()
# picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
# output = StreamingOutput()
# picam2.start_recording(JpegEncoder(), FileOutput(output))

async def handler(websocket):
    # connection_handler.add_connection(websocket)
    # await display_leds(websocket)
    print('connected')
    await connection_handler.listen(websocket)


    # async for message in websocket:
    #     await connection_handler.store(message)

def ssl_cert_and_key_exist():
    return os.path.exists(CERT_PATH) and os.path.exists(KEY_PATH)

async def main():
    # Initialize the aiohttp ClientSession
    await connection_handler.start()
    
    # Set up SSL if needed
    ssl_context = None
    if ssl_cert_and_key_exist():
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(CERT_PATH, keyfile=KEY_PATH)
        print("SSL context loaded")

    try:
        async with serve(handler, "0.0.0.0", int(sys.argv[1]), ssl=ssl_context):
            # asyncio.create_task(connection_handler.listen())
            print("Server started")
            await asyncio.get_running_loop().create_future()  # run forever
    finally:
        # Ensure the ClientSession is closed on shutdown
        await connection_handler.close()


asyncio.run(main())
