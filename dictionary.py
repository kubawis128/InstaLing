#Read Config
import config

translations = ''

def readDict():
    global translations
    file_name = config.getConf('dictionary','dict_file')
    with open(file_name,mode='r', encoding = 'utf-8') as dict:
        translations = dict.read()
    return translations

def getTransFromDict(example_usage):
    global translations
    for translate in translations.split("\n"):
        if str(example_usage) in translate:
            print(translate.strip().split("$ ",1)[1])