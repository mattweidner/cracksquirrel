# File: mod_packt.py
# Date: 2018-08-03
# Author: Matt Weidner <matt.weidner@gmail.com>
# Description: Discover and announce the Packt book of the day as advertised
#              at https://www.packtpub.com/packt/offers/free-learning
#
import datetime
import json
from lxml import html
import requests
import slack
import time

__EVENT_LOOP = None
__EXPIRE_TIME = 0
__TITLE = ""

def countdown(sec):
    time = str(datetime.timedelta(seconds=sec))
    t = time.split(":")
    return t[0]+" hrs "+t[1]+" min"

def get_commands():
    return [{"command": "packt", "callback": say_packt_book},
            {"command": "packtbook", "callback": say_packt_book}]

def grab_book():
    global __EXPIRE_TIME, __TITLE
    if int(time.time()) > __EXPIRE_TIME or __TITLE == "":
        HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0"}
        r = requests.request("GET", "https://www.packtpub.com/packt/offers/free-learning", data="", headers=HEADERS)
        page = r.content.decode("utf-8")
        tree = html.fromstring(page)
        r = tree.xpath('//div[@class="dotd-title"]/h2/text()')
        __TITLE = r[0].strip()
#       r = tree.xpath('//noscript/img[@class="bookimage imagecache imagecache-dotd_main_image"]/@src')
#       image = r[0]
        r = tree.xpath('//span[@class="packt-js-countdown"]/@data-countdown-to')
        __EXPIRE_TIME = int(r[0])
        #print("[DEBUG]", __EXPIRE_TIME, __TITLE)
        r = tree.xpath('//div[@class="dotd-title"]/h2/text()')
    return

def say_packt_book(args):
    global __TITLE, __EXPIRE_TIME
    print("[mod_packt()]", args)
    #p = await grab_book()
    grab_book()
    response = " ".join(["The current free Packt book is", '"'+__TITLE+'"', "\nThe offer will expire in", countdown(int(__EXPIRE_TIME-int(time.time()))),"\nYou can grab it here: https://www.packtpub.com/packt/offers/free-learning"])
    #print("[DEBUG]", response)
    return(response)
    #return "The packt and packtbook commands are not implemented."
    
def init():
    print("[DEBUG] [mod_packt.py] init()")
    grab_book()

async def auto_announce():
    announcement = say_packt_book({})
    slack.EVENT_LOOP.call_soon(slack.send_msg, ("GAE4LF0RH", announcement))

def main():
    #print(say_packt_book({}))
    slack.init()
    init()
    auto_announce()


if __name__ == "modules.mod_packt":
    init()

if __name__ == "__main__":
    main()
