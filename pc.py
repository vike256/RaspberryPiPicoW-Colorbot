import configparser
import socket
import cv2
import numpy
import win32api
from time import sleep
from mss import mss


## READING CONFIG START
config = configparser.ConfigParser()
config.read("config.ini")

ip = config.get('network', 'ip')
port = int(config.get('network', 'port'))

color = config.get('screen', 'color')
fov = int(config.get('screen', 'fov'))
offset = int(config.get('aim', 'offset'))
speed = float(config.get('aim', 'speed'))
xMultiplier = float(config.get('aim', 'xMultiplier'))
recoilX = float(config.get('recoil', 'recoilX'))
recoilY = float(config.get('recoil', 'recoilY'))
## READING CONFIG END


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sct = mss()
screenshot = sct.monitors[1]
screenshot['left'] = int((screenshot['width'] / 2) - (fov / 2))
screenshot['top'] = int((screenshot['height'] / 2) - (fov / 2))
screenshot['width'] = fov
screenshot['height'] = fov
center = (screenshot['width'] // 2, screenshot['height'] // 2)


toggle_aim = True
toggle_recoil = True
toggle_trigger = True

if color == 'g':
    upper_color = numpy.array([63,255,255])
    lower_color = numpy.array([58,210,80])
else:
    upper_color = numpy.array([164,255,255])
    lower_color = numpy.array([144,210,80])


def move(x, y):

    # Mouse.Move takes char (8 bytes) as input
    # 8bit signed value range is from -128 to 127
    max = 127
    if abs(x) > abs(max):
        x = x/abs(x) * abs(max)
    if abs(y) > abs(max):
        y = y/abs(y) * abs(max)

    # Raspberry checks the first character to check if the instruction is to move (M) or click (C)
    command = f"M{x},{y}\r"
    client.sendall(command.encode())
    print(f"M{x},{y} sent")
    waitForResponse()


def click():
    # Raspberry checks the first character to check if the instruction is to move (M) or click (C)
    command = "C\r"
    client.sendall(command.encode())
    print("Click sent")
    waitForResponse()

def waitForResponse():
    ack = client.recv(4).decode()
    if ack == "ACK\r":
            print("ack received")

print("Connecting")

try:
    client.connect((ip, port))

    while True:
        if win32api.GetAsyncKeyState(0xA3) < 0: # RCTRL to toggle aim
            toggle_aim = not toggle_aim
            print("AIM: " + str(toggle_aim))
            sleep(0.5)

        if win32api.GetAsyncKeyState(0xA1) < 0: #RSHIFT to toggle recoil
            toggle_recoil = not toggle_recoil
            print("RECOIL: " + str(toggle_recoil))
            sleep(0.5)

        if win32api.GetAsyncKeyState(0xA5) < 0: #RALT to toggle trigger
            toggle_trigger = not toggle_trigger
            print("TRIGGER: " + str(toggle_trigger))
            sleep(0.5)

        # AIM if mouse left or right down
        if toggle_aim and (win32api.GetAsyncKeyState(0x01) < 0 or win32api.GetAsyncKeyState(0x02) < 0):
            img = numpy.array(sct.grab(screenshot))
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower_color, upper_color)
            kernel = numpy.ones((3,3), numpy.uint8)
            dilated = cv2.dilate(mask, kernel, iterations=5)
            thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            if len(contours) != 0:
                closest_contour = None
                min_distance = float('inf')

                for contour in contours:
                    mouse = cv2.moments(contour)
                    cX = int(mouse["m10"] / mouse["m00"])
                    cY = int(mouse["m01"] / mouse["m00"])
                    distance = numpy.sqrt((cX - center[0])**2 + (cY - center[1])**2)

                    if distance < min_distance:
                        min_distance = distance
                        closest_contour = (cX, cY)
            
                if closest_contour is not None:
                    cX, cY = closest_contour

                    x = -(center[0] - cX) if cX < center[0] else cX - center[0]
                    y = -(center[1] - cY) if cY < center[1] else cY - center[1]
                    x *= speed
                    y *= speed / xMultiplier
                    y += offset
                    
                    move(x, y)

        # RECOIL
        if toggle_recoil and win32api.GetAsyncKeyState(0x01):
            move(recoilX, recoilY)
        
        sleep(0.001)
        

except KeyboardInterrupt:
    pass

finally:
    client.close()
    print("Closed")