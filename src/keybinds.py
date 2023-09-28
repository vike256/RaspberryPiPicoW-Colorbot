import win32api as wapi
from time import sleep
import setup


def check(config):
    if wapi.GetAsyncKeyState(config['reloadConfigKey']) < 0:
        config = setup.read_config()
        sct, screenshot, center = setup.setup_mss(config)
        sleep(0.5)

    if wapi.GetAsyncKeyState(config['toggleAimKey']) < 0:
        config['toggleAim'] = not config['toggleAim']
        print("AIM: " + str(config['toggleAim']))
        sleep(0.5)

    if wapi.GetAsyncKeyState(config['toggleRecoilKey']) < 0:
        config['toggleRecoil'] = not config['toggleRecoil']
        print("RECOIL: " + str(config['toggleRecoil']))
        sleep(0.5)

    if wapi.GetAsyncKeyState(config['toggleTriggerbotKey']) < 0:
        config['toggleTriggerbot'] = not config['toggleTriggerbot']
        print("TRIGGER: " + str(config['toggleTriggerbot']))
        sleep(0.5)

    return config
