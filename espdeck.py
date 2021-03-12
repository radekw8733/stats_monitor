import logging
from os import name
from SwSpotify import SpotifyClosed, SpotifyNotRunning, spotify
import SwSpotify
from osuapi import OsuApi, ReqConnector
import requests
import json
import obswebsocket, obswebsocket.requests, obswebsocket.events
from threading import Thread
import launchpad_py
from websockets import server
from radke_logging import Logger, loggingLevel
import keyboard
from time import sleep
import socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
api = OsuApi("346ab1522e56b657ada35ff7075f3553ee3fac24", connector=ReqConnector())
lp = launchpad_py.Launchpad()
obs = obswebsocket.obsws()
logger = Logger(True,"espdeck.log",3)
launchpadEnabled = False
websocketEnabled = False
if (lp.Check(0)):
    launchpadEnabled = True
    lp.Open(0)
    lp.LedCtrlXY(6,8,0,3)
    lp.LedCtrlXY(7,8,3,0)
    lp.LedCtrlXY(8,8,3,0)
    lp.LedCtrlXY(5,6,0,3)
    lp.LedCtrlXY(6,6,2,3)
    lp.LedCtrlXY(7,6,0,3)
    lp.LedCtrlXY(4,8,3,0)

def obsStartedRecording(self):
    obsRecordingStatus = True
def obsStoppedRecording(self):
    obsRecordingStatus = False

def launchpad():
    global settings
    global launchpadEnabled
    obsRecordingStatus = False
    try:
        obs.connect()
        obs.register(obsStartedRecording, event=obswebsocket.events.RecordingStarted)
        obs.register(obsStoppedRecording, event=obswebsocket.events.RecordingStopped,)
    except:
        logger.error("OBS nie jest wlaczony")
    while True:
        if (settings["launchpad"] == True and launchpadEnabled == True):
            buttons = lp.ButtonStateXY()
            if (len(buttons) > 0):
                if buttons[2] == True:
                    if buttons[0] == 6 and buttons[1] == 8:
                        keyboard.press_and_release("f13")
                    if buttons[0] == 7 and buttons[1] == 8:
                        keyboard.press_and_release("f14")
                    if buttons[0] == 8 and buttons[1] == 8:
                        if (obsRecordingStatus == False):
                            logger.info("Recording started")
                            obs.call(obswebsocket.requests.StartRecording())
                            obsRecordingStatus = True
                        else:
                            print("Recording stopped")
                            obs.call(obswebsocket.requests.StopRecording())
                            obsRecordingStatus = False
                    if buttons[0] == 4 and buttons[1] == 8:
                        keyboard.press("alt+tab")
                        sleep(0.01)
                        keyboard.release("alt+tab")
                    if buttons[0] == 6 and buttons[1] == 6:
                        pass
                    if buttons[0] == 7 and buttons[1] == 6:
                        pass
        elif (settings["launchpad"] == True and launchpadEnabled == False):
            if (lp.Check(0)):
                launchpadEnabled = True
                logger.info("Launchpad connected")
            lp.Open(0)
def music():
    try:
        currentSong = spotify.current()
    except SpotifyNotRunning:
        logger.info("Spotify not playing")
        return
    payload = {
        "type": "info",
        "firstRow": "Spotify",
        "secondRow": "Teraz jest grane"
    }
    sock.sendto(json.dumps(payload).encode(),("192.168.8.122",2137))
    sleep(1)
    payload = {
        "type": "spotify",
        "firstRow": currentSong[0],
        "secondRow": currentSong[1]
    }
    sock.sendto(json.dumps(payload).encode(),("192.168.8.122",2137))
    logger.info("Sent spotify info")
    logger.debug("Data: " + str(payload))

def osu():
    try:
        results = api.get_user("radekw8733")
    except:
        logger.error("Osu api is not available")
    payload = {
        "type": "info",
        "firstRow": "Osu!",
        "secondRow": "Moje statsy"
    }
    sock.sendto(json.dumps(payload).encode(),("192.168.8.122",2137))
    sleep(1)
    payload = {
        "type": "osu",
        "firstRow": "#" + str(results[0].pp_rank),
        "secondRow": str(results[0].pp_raw) + "pp"
    }
    sock.sendto(json.dumps(payload).encode(),("192.168.8.122",2137))
    logger.info("Sent osu data")
    logger.debug("Data: " + str(payload))

# ARDUNO STATS SEND TASK
def arduinoInfoSender():
    global settings
    while True:
        if (settings["spotify"] == True):
            music()
        sleep(settings["delay"]) 

        if (settings["osu"] == True):
            osu()
        sleep(settings["delay"])

def settingsReload():
    global settings
    while True:
        fp = open("espdeck_config.json")
        settings = json.load(fp)
        sleep(0.5)

# MAIN LOOP
if __name__ == "__main__":
    launchpadThread = Thread(target=launchpad,name="Launchpad Event Handler")
    arduinoTask = Thread(target=arduinoInfoSender,name="ESP Data Sender")
    settingsReloader = Thread(target=settingsReload,name="Settings Loader")
    settingsReloader.start()
    sleep(0.5)   # delay for settings to load
    launchpadThread.start()
    arduinoInfoSender().start()