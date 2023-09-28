import socket
import cv2
import numpy as np
import win32api as wapi
from time import sleep
import keybinds
import mouse
import screen
import setup
from key import key


def main():
    config = setup.read_config()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if config['color'] == 'g':
        upper_color = np.array([63,255,255])
        lower_color = np.array([58,210,80])
    else:
        upper_color = np.array([164,255,255])
        lower_color = np.array([144,210,80])

    print("Connecting...")

    try:
        client.connect((config['ip'], config['port']))
        print("Connected")

        while True:
            config = keybinds.check(config)

            # AIM if mouse left or right down
            if config['toggleAim'] and (wapi.GetAsyncKeyState(key['lbutton']) < 0 or wapi.GetAsyncKeyState(key['rbutton']) < 0):
                contours = screen.screengrab(config['sct'], config['screenshot'], lower_color, upper_color)

                if len(contours) != 0:
                    closest_contour = screen.get_closest_target(contours, config['center'])
                
                    if closest_contour is not None:
                        cX, cY = closest_contour

                        x = -(config['center'][0] - cX) if cX < config['center'][0] else cX - config['center'][0]
                        y = -(config['center'][1] - cY) if cY < config['center'][1] else cY - config['center'][1]
                        x *= config['speed']
                        y *= config['speed'] / config['xMultiplier']
                        y += config['offset']
                        
                        mouse.move(x, y, client)

            # RECOIL
            if config['toggleRecoil'] and wapi.GetAsyncKeyState(key['lbutton']) < 0:
                mouse.move(config['recoilX'], config['recoilY'], client)
            
            sleep(0.001)     

    except KeyboardInterrupt:
        pass

    except TimeoutError:
        print("Connection attempt failed")

    finally:
        client.close()
        print("Closed")

if __name__=="__main__":
    main()