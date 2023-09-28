import win32api as wapi
from time import sleep
import setup

delay = 0.3

def check(config):
    if wapi.GetAsyncKeyState(config['reloadConfigKey']) < 0:
        config = setup.read_config()
        sleep(delay)

    if wapi.GetAsyncKeyState(config['toggleAimKey']) < 0:
        config['toggleAim'] = not config['toggleAim']
        print("AIM: " + str(config['toggleAim']))
        sleep(delay)

    if wapi.GetAsyncKeyState(config['toggleRecoilKey']) < 0:
        config['toggleRecoil'] = not config['toggleRecoil']
        print("RECOIL: " + str(config['toggleRecoil']))
        sleep(delay)

    if wapi.GetAsyncKeyState(config['toggleTriggerbotKey']) < 0:
        config['toggleTriggerbot'] = not config['toggleTriggerbot']
        print("TRIGGER: " + str(config['toggleTriggerbot']))
        sleep(delay)

    return config