import configparser
from mss import mss
from key import key
import numpy as np

def read_config():
    configFile = configparser.ConfigParser()
    configFile.read("config.ini")
    config = {
        'toggleAim': False,
        'toggleRecoil': False,
        'toggleTriggerbot': False,
    }
    config['ip'] = configFile.get('network', 'ip')
    config['port'] = int(configFile.get('network', 'port'))
    
    if configFile.get('screen', 'color') == 'g':
        config['upper_color'] = np.array([63,255,255])
        config['lower_color'] = np.array([58,210,80])
    else:
        config['upper_color'] = np.array([164,255,255])
        config['lower_color'] = np.array([144,210,80])

    config['fov'] = int(configFile.get('screen', 'fov'))
    config['offset'] = int(configFile.get('aim', 'offset'))
    config['speed'] = float(configFile.get('aim', 'speed'))
    config['xMultiplier'] = float(configFile.get('aim', 'xMultiplier'))
    config['recoilX'] = float(configFile.get('recoil', 'recoilX'))
    config['recoilY'] = float(configFile.get('recoil', 'recoilY'))
    config['toggleAimKey'] = int(key[configFile.get('keybinds', 'toggleAimKey')])
    config['toggleRecoilKey'] = int(key[configFile.get('keybinds', 'toggleRecoilKey')])
    config['toggleTriggerbotKey'] = int(key[configFile.get('keybinds', 'toggleTriggerbotKey')])
    config['reloadConfigKey'] = int(key[configFile.get('keybinds', 'reloadConfigKey')])

    sct, screenshot, center = setup_mss(config)
    config['sct'] = sct
    config['screenshot'] = screenshot
    config['center'] = center

    print(f"""Config: 
- Network: {config['ip']}:{config['port']}
- Color: LOWER: {config['lower_color']}, UPPER: {config['upper_color']}
- FOV: {config['fov']}
- Offset: {config['offset']}
- Speed: {config['speed']}
- xMultiplier: {config['xMultiplier']}
- Recoil: ({config['recoilX']}, {config['recoilY']})
Config read, all cheats defaulted to off.""")
    return config


def setup_mss(config):
    sct = mss()
    screenshot = sct.monitors[1]
    screenshot['left'] = int((screenshot['width'] / 2) - (config['fov'] / 2))
    screenshot['top'] = int((screenshot['height'] / 2) - (config['fov'] / 2))
    screenshot['width'] = config['fov']
    screenshot['height'] = config['fov']
    center = (screenshot['width'] // 2, screenshot['height'] // 2)
    return sct, screenshot, center