import configparser
config = configparser.ConfigParser()
def loadConf():
    config.read('config.conf')
def saveConf(selection,name,toSave):
    config[selection][name] = str(toSave)
    with open('config.conf','w') as configfile:
        config.write(configfile)
def getConf(selection,name):
    conf = config[selection]
    return conf.get(name)
loadConf()