# Handle POST requests
import requests

# Parse Answers
import json

# Get unix timestamp for POST
import time

# Handle dictionary writing and reading
import dictionary

# Handle translations
from googletrans import Translator
from statistics import mode
import re 

# Read varibles from config
import config

# Get str equivalents of codes (200=OK...)
from http.client import responses

# KOLORKI UUUUUU
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Create single session
session = requests.session()

# Assign colors to status codes 200 = green
def color_http_status(status):
    if status == 200:
        return f"{bcolors.OKGREEN} {bcolors.BOLD}" + responses[status] + f"{bcolors.ENDC}"
    else:
        return f"{bcolors.FAIL} {bcolors.BOLD}" + responses[status] + f"{bcolors.ENDC}"

# Assign colors to grades anything else from 0 is green
def color_correct_answer(grade):
    if grade == 0:
        return f"{bcolors.FAIL} {bcolors.BOLD} Failed {bcolors.ENDC}"
    else:
        return f"{bcolors.OKGREEN} {bcolors.BOLD} Success {bcolors.ENDC}"

# Init Translator,login,session
def init():

    global session
    global translator

    translator = Translator()
    
    dictionary.readDict()
    url = "https://instaling.pl:443/teacher.php?page=teacherActions"
    cookies = {"PHPSESSID": "o2rvt86j7rioq7evj4lmtgfgk4", "_ga": "GA1.2.1770833722.1642012741", "_gid": "GA1.2.1767363838.1642012742", "_gat_gtag_UA_3314888_13": "1", "_fbp": "fb.1.1642012742697.1979917060", "__gads": "ID=bb24ea0d818e3273-22da7c5a1ccd0018:T=1642012743:RT=1642012743:S=ALNI_MZuPG6-J8fkdTAomahAHSsVvjIGUA"}
    headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\"Chromium\";v=\"97\", \" Not;A Brand\";v=\"99\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Linux\"", "Upgrade-Insecure-Requests": "1", "Origin": "https://instaling.pl", "Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://instaling.pl/teacher.php?page=login", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
    data = {"action": "login", "from": '', "log_email": str(config.getConf('login','login')), "log_password": config.getConf('login','passwd')}
    response = session.post(url, headers=headers, cookies=cookies, data=data) # Login

    print("Logging ended up with status code: " + color_http_status(response.status_code))

    url = "https://instaling.pl:443/ling2/server/actions/init_session.php"
    cookies = {"_ga": "GA1.2.1770833722.1642012741", "_gid": "GA1.2.1767363838.1642012742", "_fbp": "fb.1.1642012742697.1979917060", "__gads": "ID=bb24ea0d818e3273-22da7c5a1ccd0018:T=1642012743:RT=1642012743:S=ALNI_MZuPG6-J8fkdTAomahAHSsVvjIGUA", "PHPSESSID": "mg8al3kotuqu7231t9a10p05tl", "app": "app_83"}
    headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"97\", \" Not;A Brand\";v=\"99\"", "Accept": "application/json, text/javascript, */*; q=0.01", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36", "Sec-Ch-Ua-Platform": "\"Linux\"", "Origin": "https://instaling.pl", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://instaling.pl/ling2/html_app/app.php?child_id=1571488", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
    data = {"child_id": "1571488", "repeat": '', "start": '', "end": ''}
    response = session.post(url, headers=headers, cookies=cookies, data=data) #Begin Session

    print("Session start ended up with status code: " + color_http_status(response.status_code))

# Main loop
def loop():
    global session

    # We do that so python wouldn't complain about uninitalized varibles
    answer = None;
    overide = False;
    task = 0
    # Infinite Loop
    while True:
        # Get timestamp
        timestamp = int(time.time()*1000.0)

        url = "https://instaling.pl:443/ling2/server/actions/generate_next_word.php"
        cookies = {"_ga": "GA1.2.1770833722.1642012741", "_gid": "GA1.2.1767363838.1642012742", "_fbp": "fb.1.1642012742697.1979917060", "__gads": "ID=bb24ea0d818e3273-22da7c5a1ccd0018:T=1642012743:RT=1642012743:S=ALNI_MZuPG6-J8fkdTAomahAHSsVvjIGUA", "PHPSESSID": "mg8al3kotuqu7231t9a10p05tl", "app": "app_83"}
        headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"97\", \" Not;A Brand\";v=\"99\"", "Accept": "application/json, text/javascript, */*; q=0.01", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36", "Sec-Ch-Ua-Platform": "\"Linux\"", "Origin": "https://instaling.pl", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://instaling.pl/ling2/html_app/app.php?child_id=1571488", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
        data = {"child_id": "1571488", "date": timestamp}
        
        response = session.post(url, headers=headers, cookies=cookies, data=data) # Generate word
        print("Generate word ended up with status code: " + color_http_status(response.status_code))

        # print("Generate word ended up with text:" + str(response.text))
        parsed_response = json.loads(response.text)
        try:
            if parsed_response["summary"] != None:
                print(f"{bcolors.OKGREEN} {bcolors.BOLD} I'm done {bcolors.ENDC}")
                break
        except:
            print(f"{bcolors.OKGREEN} {bcolors.BOLD} Doing next excercise {bcolors.ENDC}")
        
        # If we get 2 times in the row same answer something is wrong
        try:
            if answer == dictionary.getTransFromDict(parsed_response["usage_example"]) and overide != True:
                print(f"{bcolors.FAIL} {bcolors.BOLD} Something went wrong, Failing on purpose {bcolors.ENDC}")
                answer == "sefgsreg"
                overide = True;
            else:
                # Get answer from dictionary
                answer = dictionary.getTransFromDict(parsed_response["usage_example"])
                overide = False;
        except:
            print("?")
        # If answer is not null than we have it in dict
        if answer != 0:
            final = answer

        # Else we need to download external translation
        else:
            pol_word = parsed_response["translations"]
            translation = translator.translate(pol_word,src=config.getConf('translator','from'),dest=config.getConf('translator','to'))
            if ',' in translation.text:
                # And take the most used
                final = mode(translation.text.split())
                final = re.sub("[^A-Za-zäßäÄéöÖüÜ\s]+", "",final)
                final = re.sub("[^A-Za-zäßäÄéöÖüÜ\s]+", "",final)
                final = re.sub(",", "",final)
                answer = final
            else:
                final = translation.text
                answer = final
        # Encode a response
        url = "https://instaling.pl:443/ling2/server/actions/save_answer.php"
        cookies = {"_ga": "GA1.2.1770833722.1642012741", "_gid": "GA1.2.1767363838.1642012742", "_fbp": "fb.1.1642012742697.1979917060", "__gads": "ID=bb24ea0d818e3273-22da7c5a1ccd0018:T=1642012743:RT=1642012743:S=ALNI_MZuPG6-J8fkdTAomahAHSsVvjIGUA", "PHPSESSID": "mg8al3kotuqu7231t9a10p05tl", "app": "app_83"}
        headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"97\", \" Not;A Brand\";v=\"99\"", "Accept": "application/json, text/javascript, */*; q=0.01", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36", "Sec-Ch-Ua-Platform": "\"Linux\"", "Origin": "https://instaling.pl", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://instaling.pl/ling2/html_app/app.php?child_id=1571488", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
        data = {"child_id": "1571488", "word_id": parsed_response["id"], "answer": answer, "version": "C65E24B29F60B1221EC23D979C9707DE"}
        response = session.post(url, headers=headers, cookies=cookies, data=data)

        # If we failed than learn from it and save to dictionary
        if json.loads(response.text)["grade"] == 0 or 3 or overide or json.loads(response.text)["answershow"] != answer:
            dictionary.writeToDict(parsed_response["usage_example"] + " $ " + json.loads(response.text)["answershow"])

            # And update cache
            dictionary.readDict()
        if json.loads(response.text)["grade"] != 0 or 3:
            task = task + 1
        # Print Status
        print("Save answer ended up with status code: " + color_http_status(response.status_code))
        #print("save answer ended up with text:" + str(response.text))
        print("Did we do it correctly?:" + color_correct_answer(json.loads(response.text)["grade"]))
        print(f"{bcolors.OKBLUE} I'm on " + str(task) + f"excercise {bcolors.ENDC}")
        