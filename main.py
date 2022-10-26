import filecmp
import json
import os
import shutil
import sys
import time

import requests


def optLibraries():
    try:
        import requests
    except:
        print("Installing required Libraries...")
        os.system('pip install requests')
        print("Done!")
        time.sleep(1)
        optLibraries()



cwd = os.path.dirname(os.path.realpath(__file__))
update = True

with open('./resources/dataStore.json', 'r') as fp:
    settingsJson = json.loads(fp.read())
    fp.close()

class logCol:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    
if settingsJson["runSetup"]:
    print("Running first time setup module: Anylitics")
    print("!!! Please Read !!!")
    print("This script can utilize a module that allows it to send anonymous data about what errors it finds in the player logs.")
    print("All data sent is completely anonymous (it does NOT include IP Addresses, any HWID Identifiers, Discord Account information or simmilar) and is encrypted in transit. As well as stored in a secure and encrypted manner.")
    print("This module is DISABLED by default, If you would like to enable it, type y below. If you would like to keep it disabled, type n below")
    print("Nothing else in the script will change, nor will any other features/functions of the script be effected by your decision.")
    decision = input("y/n")
    if decision == "y" or decision == "Y":
        settingsJson["runSetup"] = False
        settingsJson["anylitics"] = True
        with open('./resources/dataStore.json', 'w+') as fp:
            fp.write(json.dumps(settingsJson))
    if decision == "n" or decision == "N":
        settingsJson["runSetup"] = False
        settingsJson["anylitics"] = False
        with open('./resources/dataStore.json', 'w+') as fp:
            fp.write(json.dumps(settingsJson))

def anylitics(errors):
    if settingsJson["anylitics"]:
        length = len(errors)
        payload = {
            "findCount": length,
            "findList": errors
        }
        url = "https://api.j-stuff.net/analytics/logScanner"
        payload = json.dumps(payload)
        print("Sending analytical data...")
        x = requests.post(url, json=payload)
        print(x.text)
        if x.status_code == 200:
            print("Success!")
        else:
            print("Something went wrong while sending the analytical data. Don't worry, the service was probably down temporarilly.")
        time.sleep(3)
    else:
        print("You have opted OUT of sending analytical data.")
        time.sleep(3)





def checkForUpdates():
    print("Checking for updates, Please wait...")
    if not update:
        return
    with open('.\\resources\\dataStore.json', 'r') as fp:
        settingsJson = json.loads(fp.read())
    with open('.\\resources\\currentVersion.txt', 'r') as fp:
        scriptVersion = fp.read()
    minUrl = "https://raw.githubusercontent.com/J-Stuff/Log-Scanner/master/resources/minVersion.txt"
    minData = requests.get(minUrl)
    with open('.\\resources\\minVersion.txt', 'w+') as fp:
        fp.write(minData.text)
    with open('.\\resources\\minVersion.txt', 'r') as fp:
        minVer = fp.read()
    if minVer > scriptVersion:
        print("(!) OUTDATED (!)")
        print("This script is outdated!")
        print("A new major release has been pushed, and the auto-update cannot upgrade this version")
        print("Please download the latest version of the script at:")
        print("https://github.com/J-Stuff/Log-Scanner/releases")
        time.sleep(100)
        print("CLOSING")
        sys.exit("Outdated script!")
    unixNow = int(time.time()) 
    if int(unixNow) - int(settingsJson["lastUpdated"]) >= 86400:
        print("Checking Github for Updates...")
        translationsUrl = "https://raw.githubusercontent.com/J-Stuff/Log-Scanner/master/translations.json"
        triggersUrl = "https://raw.githubusercontent.com/J-Stuff/Log-Scanner/master/triggers.bin"
        translationsData = requests.get(translationsUrl)
        triggersData = requests.get(triggersUrl)
        with open('.\\traslations.json', 'w+') as fp:
            print("Updating Translations...")
            fp.write(translationsData.text)
        with open('.\\triggers.bin', 'w+') as fp:
            print("Updating Triggers...")
            fp.write(triggersData.text)
        time.sleep(5)
        print("Update complete!")
        settingsJson["lastUpdated"] = int(unixNow)
        with open('./resources\\dataStore.json', 'w') as fp:
            fp.write(json.dumps(settingsJson))
        time.sleep(3)
        os.system('cls')


def dedupe(mylist):
    mylist = list(dict.fromkeys(mylist))
    return mylist

def cleanup():
    os.system('cls')
    print("Cleaning up...")
    os.remove("./LogStore\\Player.log")
    time.sleep(1)
    os.system('cls')              

def checkLog(log):
    badLines = []
    with open("./triggers.bin", 'r') as triggerFile:
        triggers = triggerFile.read().splitlines()
        total = str(len(log))
        for string in log:
            for trigger in triggers:
                x = string.find(trigger)
                if x != -1:
                    badLines.append(trigger)
    time.sleep(0.2)
    os.system('cls')
    time.sleep(0.1)
    badLines = dedupe(badLines)
    if len(badLines) > 0:
        print("Errors:")
        with open("./translations.json", 'r') as fp:
            translations = json.loads(fp.read())
            fp.close()
        for error in badLines:
            try:
                message = (translations[str(error)])
                if message.startswith("(!) WARNING (!)"):
                    message = logCol.FAIL + logCol.BOLD + message + logCol.ENDC
                elif message.startswith("(i) Caution (i)"):
                    message = logCol.WARNING + message + logCol.ENDC
                print(message)
            except:
                print(f"Translation Error, Missing translation for {error}")
    else:
        print("There are no common errors found in this user's log")
    print(f"{str(total)} lines scanned.")
    print(f"With {str(len(badLines))} result(s) found.")
    anylitics(badLines)
    input("PRESS ENTER TO CONTINUE   ")
    cleanup()

def downloadLog():
    if not os.path.exists("./LogStore"):
        os.mkdir("./LogStore")
        print("Created LogStore Directory (First Time Setup)")
    print("Drag and drop the Player.log download link below")
    text = "Ctrl + Click me if you don't know how to do that"
    target = "https://cdn.discordapp.com/attachments/1019358536733569054/1028261000207683644/Untitled_video_-_Made_with_Clipchamp_2.gif"
    print(f"\u001b]8;;{target}\u001b\\{text}\u001b]8;;\u001b\\")
    url = input('Enter the URL of the Player.log: ')
    logData = requests.get(url, allow_redirects=True)
    with open(".\\LogStore\\Player.log", 'wb') as fp:
        fp.write(logData.content)


def getLog():
    checkForUpdates()
    downloadLog()
    if os.path.exists("./LogStore\\Player.log"):
        print("Found log!")
        print("Reading...")
        with open("./LogStore\\Player.log", 'r') as fp:
            logContents = fp.read().splitlines()
            fp.close()
            checkLog(logContents)
    else:
        print("Couldn't find a player log??")
        print("Caught an error that technically shouldn't exist")
        time.sleep(10)

if __name__ in "__main__":
    getLog()

# BUFFER