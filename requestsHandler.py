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
    global cookies
    global child_id

    translator = Translator()
    dictionary.readDict()

    # Create single session
    session = requests.session()
    session.cookies.clear()

    headers = {'user-Agent': 'Mozilla/5.0'}

    url = "https://instaling.pl:443/teacher.php?page=login"
    response = session.get(url, headers=headers)
    phpsessid = response.headers['Set-Cookie'].split(";")[0].split("=")[1]

    url = "https://instaling.pl:443/teacher.php?page=teacherActions"
    data = {"action": "login", "from": '', "log_email": config.getConf("login", "login"), "log_password": str(config.getConf('login','passwd'))}
    response = session.post(url, headers=headers, data=data, allow_redirects=False) # Login
    phpsessid = response.headers['Set-Cookie'].split(";")[0].split("=")[1]

    print("Logging ended up with status code: " + color_http_status(response.status_code))

    url = "https://instaling.pl:443/learning/dispatcher.php?from="
    response = session.get(url, headers=headers, allow_redirects=False)
    child_id = response.headers['Location'].split("=")[1]

    url = "https://instaling.pl:443/student/pages/mainPage.php?student_id=" + str(child_id)
    response = session.get(url, headers=headers)

    url = "https://instaling.pl:443/ling2/server/actions/init_session.php"
    data = {"child_id": child_id, "repeat": '', "start": '', "end": ''}
    response = session.post(url, headers=headers, data=data) #Begin Session

    print("Session start ended up with status code: " + color_http_status(response.status_code))
    
# Main loop
def loop():
    global session
    global cookies
    global child_id

    # We do that so python wouldn't complain about uninitalized varibles
    answer = None;
    overide = False;
    task = 0
    headers = {'user-Agent': 'Mozilla/5.0'}

    # Infinite Loop
    while True:
        # Get timestamp
        timestamp = int(time.time()*1000.0)
        url = "https://instaling.pl:443/ling2/server/actions/generate_next_word.php"
        data = {"child_id": child_id, "date": timestamp}

        response = session.post(url, headers=headers, data=data) # Generate word
        print("Generate word ended up with status code: " + color_http_status(response.status_code))

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
        time.sleep(0.45 * len(answer))


        url = "https://instaling.pl:443/ling2/server/actions/save_answer.php"
        data = {"child_id": child_id, "word_id": parsed_response["id"], "answer": answer, "version": "C65E24B29F60B1221EC23D979C9707DE"}
        response = session.post(url, headers=headers, data=data) # Generate word

        print("Save answer ended up with status code: " + color_http_status(response.status_code))

        # If we failed than learn from it and save to dictionary
        if json.loads(response.text)["grade"] == 0 or 3 or overide or json.loads(response.text)["answershow"] != answer:
            dictionary.writeToDict(parsed_response["usage_example"] + " $ " + json.loads(response.text)["answershow"])

            # And update cache
            dictionary.readDict()
        if json.loads(response.text)["grade"] != 0 or 3:
            task = task + 1

        # Print Status
        print("Did we do it correctly?:" + color_correct_answer(json.loads(response.text)["grade"]))
        print(f"{bcolors.OKBLUE} I'm on " + str(task) + f" excercise {bcolors.ENDC}")
        