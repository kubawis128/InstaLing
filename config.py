import configparser
config = configparser.ConfigParser()
def loadConf():
    config.read('config.conf')
def getConf(selection,name):
    conf = config[selection]
    return conf.get(name)
loadConf()