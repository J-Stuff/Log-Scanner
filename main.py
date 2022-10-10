import json
import sys
import time
import os

cwd = os.path.dirname(os.path.realpath(__file__))

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
                print(translations[str(error)])
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

# Buffer                                           