#Read Config
import config
#Get or save words
import dictionary
#Browser stuff
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    content = driver.find_element_by_class_name('sesion')
    driver.get(content.get_attribute("href"))
    WebDriverWait(driver, 1000).until(EC.invvisibility_of(driver.find_element_by_class_name('big_button')))

# Starts exercises
def start():
    pol_word = driver.find_element_by_class_name('translations').text
    example_usage = driver.find_element_by_class_name('usage_example').text
