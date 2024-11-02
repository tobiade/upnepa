import asyncio
import websockets
import json

async def send_message():
    uri = "ws://localhost:8765"
    message = {
        "ledStates": {
            "0": [0, 1, 2, 3, 4, 5],
            "1": [6,7],
            "2": [0,1,2,3,4,5,6,7],
            "3": [0,1,2,3,4,5,6,7],
            "7": [1,2,3]


        }
        }
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(message))
        while True:
            response = await websocket.recv()
            print(f"Received response: {response}")

if __name__ == "__main__":
    asyncio.run(send_message())