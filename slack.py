# File: slack.py
# Date: 2018-08-03
# Author: Matt Weidner <matt.weidner@gmail.com>
# Description: Slackbot RTM API
#

import asyncio
import json
import os
import requests
import time
import websockets

__API_KEY = ""
__SELF = {}
__TEAM = {}
__WSS_URL = ""
__SOCKET = None
__CALLBACK = None
__LAST_ACTIVITY = None
__PING_INTERVAL = 15

def connect(callback):
    global __API_KEY, __SELF, __TEAM, __WSS_URL, __SOCKET, __CALLBACK, __LAST_ACTIVITY
    if __API_KEY == "":
        print("[!] slack.connect() No API key!")
        return False
    __CALLBACK = callback
    headers = { "Content-Type": "application/x-www-form-urlencoded"}
    r = requests.request("GET", "https://slack.com/api/rtm.connect?token="+__API_KEY)
    c = r.content.decode("utf-8")
    j = json.loads(c)
    if j["ok"] == False:
        return False
    __SELF = j["self"]
    __TEAM = j["team"]
    __WSS_URL = j["url"]
    __LAST_ACTIVITY = time.time()
    tasks = asyncio.gather(sniff(), ping())
    asyncio.get_event_loop().run_until_complete(tasks)

async def sniff():
    global __LAST_ACTIVITY, __SOCKET
    async with websockets.connect(__WSS_URL, ssl=True) as ws:
        __SOCKET = ws
        while True:
            try:
                m = await __SOCKET.recv()
                update_activity()
                __CALLBACK(m)
            except websockets.exceptions.ConnectionClosed as e:
                print("[!] sniff() Socket closed. reconnecting...", time.time())
                try:
                    time.sleep(5)
                    __SOCKET = websockets.connect(__WSS_URL, ssl=True)
                    print("[+]     sniff() Reconnected at", time.time())
                except Exception as e:
                    print("[!]     sniff() Re-connect failed!", e)

async def ping():
    while True:
        elapsed = int(time.time() - __LAST_ACTIVITY)
        #print("[DEBUG] ping() last activity:", elapsed)
        if elapsed >= __PING_INTERVAL:
            update_activity()
            elapsed = 0
            #print("[DEBUG] ping()")
            try:
                __SOCKET.ping()
            except:
                pass
        #print("[DEBUG] ping() sleeping", __PING_INTERVAL-elapsed)
        await asyncio.sleep(__PING_INTERVAL-elapsed)

def update_activity():
    global __LAST_ACTIVITY
    __LAST_ACTIVITY = time.time()

def disconnect():
    pass

def send_msg():
    update_activity()
    print("[DEBUG] slack.send_msg()", __LAST_ACTIVITY)

def init():
    global __API_KEY
    try:
        __API_KEY = os.environ["SLACK_API_KEY"]
    except KeyError:
        print("[!] slack.init() No SLACK_API_KEY env var set.")
        __API_KEY = ""
    #print("[DEBUG] SLACK_API_KEY from env:", API_KEY)

def main():
    print(__API_KEY)

if __name__ == "slack":
    init()

if __name__ == "__main__":
    main()
