from os import read
from gpiozero import OutputDevice
import time
from flask import Flask, request, jsonify
from threading import Lock, Thread
from gpiozero import LED
from typing import List, Dict, Tuple, Any, Optional
import json


import redis
from redis import Redis

from constants import LED_CHANNEL, LED_QUEUE
from led_matrix import LEDMatrix

app = Flask(__name__)

LSBFIRST = 1
MSBFIRST = 2

# define the pins connect to 74HC595
dataPin   = OutputDevice(17)      # DS Pin of 74HC595(Pin14)
latchPin  = OutputDevice(27)      # ST_CP Pin of 74HC595(Pin12)
clockPin  = OutputDevice(22)      # CH_CP Pin of 74HC595(Pin11)

class LEDController:
    def __init__(self) -> None:
        self.leds: List[int] = [0,0,0,0,0,0,0,0]
    # The tuple is (column, value) where value represents the leds that should be on
    def set_leds(self, on: List[Tuple[int,int]], off: List[Tuple[int,int]]) -> Dict[str, Dict[str, List[int]]]:
        # perform this validation earlier
        for index, value in on:
            if not (0 <= value <= 255):
                raise ValueError(f"Value must be an 8-bit number (0-255), got {value}")
            if not (0 <= index < 8):
                raise ValueError(f"Index must be between 0 and 7, got {index}")
            self.leds[index] |= value
        for index, value in off:
            if not (0 <= value <= 255):
                raise ValueError(f"Value must be an 8-bit number (0-255), got {value}")
            if not (0 <= index < 8):
                raise ValueError(f"Index must be between 0 and 7, got {index}")
            self.leds[index] &= ~value
        return self.led_states()


    def shiftOut(self, val):
        #  Shifts bits out from MSB to LSB
        for i in range(0,8):
            clockPin.off()
            bitIsHigh = 0x80 & (val << i) == 0x80
            dataPin.on() if bitIsHigh else dataPin.off()
            clockPin.on()

    def start_display(self):
        while True:
            # for j in range(0,500): # Repeat enough times to display the smiling face a period of time
                x=0x80
                for i in range(0,8):
                    latchPin.off()
                    self.shiftOut(self.leds[i]) #first shift data of line information to first stage 74HC959

                    self.shiftOut(~x) #then shift data of column information to second stage 74HC959
                    latchPin.on()         # Output data of two stage 74HC595 at the same time
                    time.sleep(0.001) # display the next column
                    x>>=1
    def destroy(self):  
        dataPin.close()
        latchPin.close()
        clockPin.close()
    
    def led_states(self) -> Dict[str, Dict[str, List[int]]]:
        """
        Returns the current state of the LEDs. The dictionary is of the form {"on": {"0": [1,7]}, "off": {"1": [2,3,4,5,6]}}
        """
        on = {}
        off = {}
        for i in range(8):
            on_list = [7-j for j in range(8) if (self.leds[i] >> j) & 1] # We use 7-j to invert the row order so it displays on the LEDs correctly
            off_list = [7-j for j in range(8) if not (self.leds[i] >> j) & 1]
            if on_list:
                on[str(i)] = on_list
            if off_list:
                off[str(i)] = off_list
        
        return {"on": on, "off": off}
    
led_controller = LEDController()


def read_led_state_from_queue(redisUrl: str, batch_size: int) -> None:
    redisClient = redis.from_url(redisUrl)
    while True:
        with redisClient.pipeline() as pipe:
            try:
                for _ in range(batch_size):
                    pipe.rpop(LED_QUEUE)
                messages = pipe.execute()
                if messages is not None:
                    for message in messages:
                        if message is None:
                            continue
                        leds = json.loads(message.decode('utf-8'))
                        print("received message:", leds)
                        ledStates = LEDMatrix(leds['ledStates'])
                        onAndOff = ledStates.serialize_to_bitmask()
                        led_controller.set_leds(onAndOff["on"], onAndOff["off"])
            except Exception as e:
                print(e)
        #  Publish led_state to Redis channel
        response = {'ledStates': led_controller.led_states()}
        redisClient.publish(LED_CHANNEL, json.dumps(response))
        time.sleep(0.05)

if __name__ == '__main__':
    try:
        # Start the LED update loop in a separate thread
        update_thread = Thread(target=led_controller.start_display, daemon=True)
        update_thread.start()
        
        # app.run(host='0.0.0.0', port=5000, debug=False)
        read_led_state_from_queue('redis://localhost', 10)
    except KeyboardInterrupt:
        led_controller.destroy()
        pass
