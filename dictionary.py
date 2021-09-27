#Read Config
import config

#Load dictionary to varible
def readDict():
    global translations
    file_name = config.getConf('dictionary','dict_file')
    with open(file_name,mode='r', encoding = 'utf-8') as dict:
        translations = dict.read()
    return translations

#Get Translations from dictionary
def getTransFromDict(example_usage):
    global translations
    for translate in translations.split("\n"):
        if example_usage in translate:
            return translate.strip().split("$ ",1)[1]
    else:
        return 0
def writeToDict(word_to_write):
    file_name = config.getConf('dictionary','dict_file')
    with open(file_name,mode='a', encoding = 'utf-8') as dict:
        dict.write("\n" + str(word_to_write))
readDict()