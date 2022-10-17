import filecmp
import json
import os
import shutil
import sys
import time

cwd = os.path.dirname(os.path.realpath(__file__))
update = True
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

def checkForUpdates():
    print("Checking for updates, Please wait...")
    if not update:
        return
    with open('.\\resources\\dataStore.json', 'r') as fp:
        settingsJson = json.loads(fp.read())
    with open('.\\resources\\currentVersion.txt', 'r') as fp:
        scriptVersion = fp.read()
    minUrl = "https://raw.githubusercontent.com/J-Stuff/Log-Scanner/master/resources/minVersion.txt"
    os.system(f"curl.exe -s -o \".\\resources\\minVersion.txt\" {minUrl}")
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
    if int(unixNow) - int(settingsJson["lastUpdated"]) >= 172800:
        print("Checking Github for Updates...")
        

        translationsUrl = "https://raw.githubusercontent.com/J-Stuff/Log-Scanner/master/translations.json"
        triggersUrl = "https://raw.githubusercontent.com/J-Stuff/Log-Scanner/master/triggers.bin"
        os.mkdir("./temp")
        os.system(f"curl.exe -s -o \"{cwd}\\temp\\translationsGithub.tmp\" {translationsUrl}")
        os.system(f"curl.exe -s -o \"{cwd}\\temp\\triggersGithub.tmp\" {triggersUrl}")
        translationsMatch = filecmp.cmp(f"{cwd}\\temp\\translationsGithub.tmp", "./translations.json")
        print(translationsMatch)
        triggersMatch = filecmp.cmp(f"{cwd}\\temp\\triggersGithub.tmp", "./triggers.bin")
        print(triggersMatch)
        if not translationsMatch:
            print("Updating translations...")
            os.system(f"curl.exe -s -o \"{cwd}\\translations.json\" {translationsUrl}")
        if not translationsMatch:
            print("Updating triggers...")
            os.system(f"curl.exe -s -o \"{cwd}\\triggers.bin\" {triggersUrl}")
        time.sleep(5)
        print("Update complete!")
        shutil.rmtree(f'{cwd}\\temp')
        settingsJson["lastUpdated"] = int(unixNow)
        with open('.\\resources\\dataStore.json', 'w') as fp:
            fp.write(json.dumps(settingsJson))
        time.sleep(3)
        try:
            shutil.rmtree(f'{cwd}\\temp')
        except:
            print("Cleanup")
        os.system('cls')


def dedupe(mylist):
    mylist = list(dict.fromkeys(mylist))
    return mylist

def cleanup():
    os.system('cls')
    print("Cleaning up...")
    os.remove(f"{cwd}\\LogStore\\Player.log")
    time.sleep(1)
    os.system('cls')              

def checkFile(input):
    for line in input:
        x = line.find("Loaded NorthwoodLib")
        if x != -1:
            print("File is Valid!")
            time.sleep(0.3)
            return
    os.system('cls')
    print("This file is not a valid player.log file!")
    print("Please ensure that you provided a valid player.log URL")
    print("If you know you provided a valid player.log file, Please file a bug report with the developer!")
    time.sleep(10)
    sys.exit("Didn't provide a valid Player.log file!")

def checkLog(log):
    checkFile(log)
    badLines = []
    with open(f"{cwd}\\triggers.bin", 'r') as triggerFile:
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
        with open(f"{cwd}\\translations.json", 'r') as fp:
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
    input("PRESS ENTER TO CONTINUE   ")
    cleanup()

def downloadLog():
    if not os.path.exists(f"{cwd}\\LogStore"):
        os.mkdir(f"{cwd}\\LogStore")
        print("Created LogStore Directory (First Time Setup)")
    print("Drag and drop the Player.log download link below")
    text = "Ctrl + Click me if you don't know how to do that"
    target = "https://cdn.discordapp.com/attachments/1019358536733569054/1028261000207683644/Untitled_video_-_Made_with_Clipchamp_2.gif"
    print(f"\u001b]8;;{target}\u001b\\{text}\u001b]8;;\u001b\\")
    os.system(f"curl.exe -o \"{cwd}\\LogStore\\Player.log\" {input('Enter the URL of the Player.log: ')}")

def getLog():
    checkForUpdates()
    downloadLog()
    if os.path.exists(f"{cwd}\\LogStore\\Player.log"):
        print("Found log!")
        print("Reading...")
        with open(f"{cwd}\\LogStore\\Player.log", 'r') as fp:
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