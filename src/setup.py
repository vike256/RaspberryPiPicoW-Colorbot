import configparser
from mss import mss
from key import key

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
    config['color'] = configFile.get('screen', 'color')
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
    print(f"""Read config 
- Network: {config['ip']}:{config['port']}
- Color: {config['color']}
- FOV: {config['fov']}
- Offset: {config['offset']}
- Speed: {config['speed']}
- xMultiplier: {config['xMultiplier']}
- Recoil: ({config['recoilX']}, {config['recoilY']})""")
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