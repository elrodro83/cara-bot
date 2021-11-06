import websocket
import _thread
#import time
import json
from adafruit_servokit import ServoKit
from time import sleep
#from pprint import pprint

class JoystickPosition(object):
    def __init__(self, x, y, speed, angle):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)

panAngle = 0
tltAngle = 0

panServo = kit.servo[0]
tltServo = kit.servo[1]

pos = JoystickPosition(0,0,0,0)

def on_message(ws, message):
    global pos
    print(message)
    #pprint(vars(message))
    j = json.loads(message)
    pos = JoystickPosition(**j)
    print("x: " + str(pos.x))
    print("y: " + str(pos.y))
    print("v: " + str(pos.speed))

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        global pos
        global panAngle
        global panServo
        global tltAngle
        global tltServo
        while True:
            panAngle = panAngle + ((pos.x * -1) / 200)
            tltAngle = tltAngle + ((pos.y) / 200)

            if panAngle < -75:
                panAngle = -75
            if panAngle > 75:
                panAngle = 75
            if tltAngle < -75:
                tltAngle = -75
            if tltAngle > 75:
                tltAngle = 75

            print("pan: " + str(panAngle))
            print("tlt: " + str(tltAngle))

            panServo.angle = panAngle + 75
            tltServo.angle = tltAngle + 75

#            sleep(1)
#        for i in range(3):
#            time.sleep(1)
#            ws.send("Hello %d" % i)
#        time.sleep(1)
#        ws.close()
#        print("thread terminating...")
    _thread.start_new_thread(run, ())
#    pass

if __name__ == "__main__":
#    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://192.168.66.137:8000/",
#    ws = websocket.WebSocketApp("ws://echo.websocket.org/",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever()
    ws.close()





#kit.servo[0].angle = 175
#sleep(1)
#kit.servo[1].angle = 45
#sleep(1)

