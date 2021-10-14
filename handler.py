# Read Config
import config

# Get or save words
import dictionary

# Browser stuff
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# import for most used word
from statistics import mode

# Google Translator
from googletrans import Translator

# REGEX
import re 

# Spanko
from time import sleep

# Setup Browser
# Reads config and selects 
def setupBrowser():
    global driver
    browser = config.getConf('browser','browser')
    if browser == "Firefox":
        driver = webdriver.Firefox()
    elif browser == "Chrome":
        driver = webdriver.Chrome()
    elif browser == "Edge":
        driver = webdriver.Edge()
    elif browser == None:
        print("Update config!\nMissing browser selection!")

# Load Page
# Waits until you are logged in
def setupPage():
    global driver
    driver.get(config.getConf('browser','login'))
    WebDriverWait(driver, 1000).until(EC.url_contains(config.getConf('browser','home')))

# Begins Session
# Loads into session
def beginSession():
    WebDriverWait(driver, 1000).until(EC.visibility_of_element_located((By.CLASS_NAME, 'sesion')))
    content = driver.find_element_by_class_name('sesion')
    driver.get(content.get_attribute("href"))
    try:
        driver.find_element_by_id('continue_session_page').click()
    except:
        driver.find_element_by_id('start_session_button').click()
    WebDriverWait(driver, 1000).until(EC.invisibility_of_element_located((By.ID, 'continue_session_page')))
    driver.find_element_by_id('start_session_button').click()

# Starts exercises
def start():
    global example_usage
    dictionary.readDict()
    WebDriverWait(driver, 1000).until(EC.visibility_of_element_located((By.CLASS_NAME, 'usage_example')))
    example_usage = driver.find_element_by_class_name('usage_example').text
    answer = dictionary.getTransFromDict(example_usage)
    if driver.find_element('id','answer').get_attribute('value') == "":
        if answer != 0:
            driver.find_element_by_id('answer').send_keys(str(answer))
        else:
            pol_word = driver.find_element_by_class_name('translations').text
            translation = translator.translate(pol_word,src='pl',dest='de')
            final = mode(translation.text.split())
            if ',' in translation.text:
                final = re.sub("[^A-Za-zäßäÄéöÖüÜ\s]+", "",final)
            final = re.sub("[^A-Za-zäßäÄéöÖüÜ\s]+", "",final)
            final = re.sub(",", "",final)
            driver.find_element_by_id('answer').send_keys(str(final))
            checkIfOk()

# Checks if answer was ok
def checkIfOk():
    global driver
    global example_usage
    WebDriverWait(driver, 1000).until(EC.visibility_of_element_located((By.ID, 'word')))
    try:
        driver.find_element_by_class_name('green')
        driver.find_element_by_class_name('red')
    except:
        if driver.find_element_by_id('word').text == "":
            driver.execute_script("alert('EMM... odowiedz jest pusta HELP');")
        else:
            final = example_usage + " $ " + driver.find_element_by_id('word').text
            dictionary.writeToDict(final)
def exit():
    global driver
    try:
        driver.close()
        driver.quit()
    except:
        return 0 

# Init function
def init():
    global translator
    translator = Translator()
    setupBrowser()
    setupPage()
    beginSession()