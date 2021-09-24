import configparser
config = configparser.ConfigParser()
def loadConf():
    config.read('config.conf')
def getBrowserConf(name):
    browser = config['browser']
    return browser.get(name)
loadConf()