import asyncio
import json
import websockets

# Define the WebSocket URL
WS_URL = "wss://upnepa.live:8765"

# Define the JSON data to send
led_states_json1 = {
    "ledStates": {
        "on": {
            "2": [0]
        }
    }
}
led_states_json2 = {
    "ledStates": {
        "on": {
            "5": [0]
        }
    }
}

async def send_led_states():
    try:
        # Establish the WebSocket connection
        async with websockets.connect(WS_URL) as websocket:
            print(f"Connected to {WS_URL}")

            # Convert the Python dictionary to a JSON string
            json_data1 = json.dumps(led_states_json1)
            json_data2 = json.dumps(led_states_json2)
            # print(f"Sending data: {json_data1}")

            # Send the JSON data
            await asyncio.gather(
                websocket.send(json_data1),
                websocket.send(json_data2)
            )
            # await websocket.send(json_data1)
            # sleep(0.5)
            # await websocket.send(json_data2)
            print("sent data")
            # Await a response from the server (optional)
            # try:
            #     response = await asyncio.wait_for(websocket.recv(), timeout=5)
            #     print(f"Received message: {response}")
            # except asyncio.TimeoutError:
            #     print("No response received within timeout period.")

    except websockets.exceptions.InvalidURI:
        print(f"Invalid WebSocket URI: {WS_URL}")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed with error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    asyncio.run(send_led_states())

if __name__ == "__main__":
    main()
