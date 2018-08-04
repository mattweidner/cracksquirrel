# File: slack.py
# Date: 2018-08-03
# Author: Matt Weidner <matt.weidner@gmail.com>
# Description: Slackbot RTM API
#

import asyncio
import functools
import json
import os
import requests
import signal
import time
import websockets

__API_KEY = ""
__EVENT_LOOP = None
SELF = {}
__TEAM = {}
__WSS_URL = ""
__SOCKET = None
__CALLBACK = None
__LAST_ACTIVITY = None
__PING_INTERVAL = 15

def connect(callback):
    global __API_KEY, SELF, __TEAM, __WSS_URL, __SOCKET, __CALLBACK, __LAST_ACTIVITY, __EVENT_LOOP
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
    SELF = j["self"]
    __TEAM = j["team"]
    __WSS_URL = j["url"]
    __LAST_ACTIVITY = time.time()
    __EVENT_LOOP = asyncio.get_event_loop()

    for sig in ('SIGINT', 'SIGTERM'):
        __EVENT_LOOP.add_signal_handler(getattr(signal, sig), functools.partial(terminate, sig))
    tasks = [__EVENT_LOOP.create_task(sniff()),__EVENT_LOOP.create_task(ping())]
    asyncio.gather(*tasks)
    print("[+] Ready.")
    try:
        __EVENT_LOOP.run_forever()
    finally:
        __EVENT_LOOP.close()

def terminate(sig):
    __EVENT_LOOP.stop()


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
                print("[!] sniff() Socket closed. terminating.", time.time())
                terminate('SIGINT')

async def ping():
    while True:
        elapsed = int(time.time() - __LAST_ACTIVITY)
        #print("[DEBUG] ping() last activity:", elapsed)
        if elapsed >= __PING_INTERVAL:
            update_activity()
            elapsed = 0
            #print("[DEBUG] ping()")
            try:
                await __SOCKET.ping()
            except:
                print("[!] ping failed.")
                pass
        #print("[DEBUG] ping() sleeping", __PING_INTERVAL-elapsed)
        await asyncio.sleep(__PING_INTERVAL-elapsed)

def update_activity():
    global __LAST_ACTIVITY
    __LAST_ACTIVITY = time.time()

def send_msg(message):
    update_activity()
    print("[DEBUG] slack.send_msg()", __LAST_ACTIVITY)
    try:
        print("[DEBUG] sending msg:", message)
    except websockets.exceptions.ConnectionClosed as e:
        print("[!] sniff() Socket closed. terminating.", time.time())
        terminate('SIGINT')

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
