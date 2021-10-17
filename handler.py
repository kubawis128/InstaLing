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
import gui
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
    driver.find_element('id','log_email').send_keys(str(config.getConf('login','login')))
    driver.find_element('id','log_password').send_keys(str(config.getConf('login','passwd')))
    driver.find_element('css selector',"button.btn.btn-primary.w-100.mt-3.mb-3").click()
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
    try:
        driver.find_element_by_id('start_session_button').click()
    except:
        pass

# Starts exercises
def start():
    global example_usage
    dictionary.readDict()
    try:
        WebDriverWait(driver, 1000).until(EC.visibility_of_element_located((By.CLASS_NAME, 'usage_example')))
    except:
        pass
    example_usage = driver.find_element_by_class_name('usage_example').text
    answer = dictionary.getTransFromDict(example_usage)
    if driver.find_element('id','answer').get_attribute('value') == "":
        if answer != 0:
            driver.find_element_by_id('answer').send_keys(str(answer))
            if config.getConf('automode','fullAuto') == "true":
                driver.find_element('id','check').click()
                sleep(float(config.getConf('automode','sleepAuto')))
                driver.find_element('id','nextword').click()
                return 0
        else:
            pol_word = driver.find_element_by_class_name('translations').text
            translation = translator.translate(pol_word,src=config.getConf('translator','from'),dest=config.getConf('translator','to'))
            final = mode(translation.text.split())
            if ',' in translation.text:
                final = re.sub("[^A-Za-zäßäÄéöÖüÜ\s]+", "",final)
            final = re.sub("[^A-Za-zäßäÄéöÖüÜ\s]+", "",final)
            final = re.sub(",", "",final)
            driver.find_element_by_id('answer').send_keys(str(final))
            if config.getConf('automode','fullAuto') == "true":
                sleep(float(config.getConf('automode','sleepAuto')))
                driver.find_element('id','check').click()
            checkIfOk()
            return 0
    else:
        return 0
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
            try:
                driver.execute_script("alert('EMM... odowiedz jest pusta HELP');")
                gui.auto_solve()
                return 0 
            except:
                pass
                return 0 
        else:
            final = example_usage + " $ " + driver.find_element_by_id('word').text
            dictionary.writeToDict(final)
            if config.getConf('automode','fullAuto') == "true":
                sleep(float(config.getConf('automode','sleepAuto')))
                driver.find_element('id','nextword').click()
            return 0
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