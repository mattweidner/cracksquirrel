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
import urllib.parse
import websockets

__API_KEY = ""
EVENT_LOOP = None
SELF = {}
__TEAM = {}
__WSS_URL = ""
__SOCKET = None
__CALLBACK = None
__LAST_ACTIVITY = None
__PING_INTERVAL = 15

def connect(callback):
    global __API_KEY, SELF, __TEAM, __WSS_URL, __SOCKET, __CALLBACK, __LAST_ACTIVITY, EVENT_LOOP
    if __API_KEY == "":
        print("[!] slack.connect() No API key!")
        return False
    __CALLBACK = callback
    headers = { "Content-Type": "application/x-www-form-urlencoded"}
    r = requests.request("GET", "https://slack.com/api/rtm.connect?token="+__API_KEY)
    c = r.content.decode("utf-8")
    j = json.loads(c)
    if j["ok"] == False:
        print(j)
        return False
    SELF = j["self"]
    __TEAM = j["team"]
    __WSS_URL = j["url"]
    __LAST_ACTIVITY = time.time()
    print("[+] TEAM:", __TEAM)
    print("[+]  BOT:", SELF)

    for sig in ("SIGINT", "SIGTERM"):
        EVENT_LOOP.add_signal_handler(getattr(signal, sig), functools.partial(terminate, sig))
    tasks = [EVENT_LOOP.create_task(sniff()),EVENT_LOOP.create_task(ping())]
    #asyncio.gather(*tasks)
    try:
        EVENT_LOOP.run_forever()
    finally:
        EVENT_LOOP.close()

def terminate(sig):
    EVENT_LOOP.stop()


async def sniff():
    global __LAST_ACTIVITY, __SOCKET
    async with websockets.connect(__WSS_URL, ssl=True) as ws:
        __SOCKET = ws
        while True:
            try:
                m = await __SOCKET.recv()
                update_activity()
                await __CALLBACK(m)
            except websockets.exceptions.ConnectionClosed as e:
                print("[!] sniff() Socket closed. terminating.", time.time())
                terminate("SIGINT")

async def ping():
    while True:
        elapsed = int(time.time() - __LAST_ACTIVITY)
        #print("[DEBUG] ping() last activity:", elapsed)
        if elapsed >= __PING_INTERVAL:
            update_activity()
            elapsed = 0
            #print("[DEBUG] ping()")
            try:
                if __SOCKET is None:
                    terminate("SIGINT")
                await __SOCKET.ping()
            except websockets.exceptions.ConnectionClosed:
                terminate("SIGINT")
            except Exception as e:
                print("[!] ping failed.")
                print("[!]     ", e)
        #print("[DEBUG] ping() sleeping", __PING_INTERVAL-elapsed)
        await asyncio.sleep(__PING_INTERVAL-elapsed)

def update_activity():
    global __LAST_ACTIVITY
    __LAST_ACTIVITY = time.time()

async def send_attachment(message):
    for attachment in message["attachments"]:
        if "image_url" in attachment.keys():
            attachment["image_url"] = attachment["image_url"].replace(" ", "%20")
    attachments = urllib.parse.quote(json.dumps(message["attachments"]))
    # 'username': 'bot', 'bot_id': 'B9QAEBQUR'
    url = "https://slack.com/api/chat.postMessage?token="+__API_KEY+"&channel="+message["channel"]+"&as_user=true&username="+SELF["name"]+"&bot_id="+SELF["id"]+"&attachments="+attachments+"&text=\""+message["text"]+"\""
    print("[DEBUG] send_attachment:", message)
    print("[DEBUG] send_attachment:", url)
    r = requests.request("GET", url)
    print(r.json())

async def send_msg(channel, message):
    global __SOCKET
    if __SOCKET is None:
        return
    update_activity()
    msg = ""
    #print("[DEBUG] slack.send_msg()", __LAST_ACTIVITY)
    print("[DEBUG] slack.send_msg()", message)
    if type(message) is str:
        try:
            # Unmarshall from json string
            msg = json.loads(message)
        except:
            # message is not a json string, create a Slack json
            # message.
            msg = {"id": int(time.time()*100), "type": "message", "channel": channel, "text": message}
    else:
        return
    if "channel" not in msg.keys():
        msg["channel"] = channel

    print("[DEBUG] send_msg: channel", msg["channel"])
    # attachments are not supported using thr RTM API websocket
    # You MUST send these using the chat.postMessage method URL
    # https://slack.com/api/chat.postMessage
    if "attachments" in msg.keys():
        # Send using chat.postMessage
        await send_attachment(msg)
        return
    # Send the json frame
    try:
        print("[DEBUG] send_msg():", msg)
        await __SOCKET.send(json.dumps(msg))
    except websockets.exceptions.ConnectionClosed as e:
        print("[!] slack.send_msg() Socket closed. terminating.", time.time())
        terminate('SIGINT')

def init():
    global __API_KEY, EVENT_LOOP
    try:
        __API_KEY = os.environ["SLACK_API_KEY"]
    except KeyError:
        print("[!] slack.init() No SLACK_API_KEY env var set.")
        __API_KEY = ""
    EVENT_LOOP = asyncio.get_event_loop()
    #print("[DEBUG] SLACK_API_KEY from env:", __API_KEY)

def main():
    init()
    print(__API_KEY)

if __name__ == "slack":
    init()

if __name__ == "__main__":
    main()
