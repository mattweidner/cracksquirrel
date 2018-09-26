# File: mod_packt.py
# Date: 2018-08-03
# Author: Matt Weidner <matt.weidner@gmail.com>
# Description: Discover and announce the Packt book of the day as advertised
#			   at https://www.packtpub.com/packt/offers/free-learning
#
import asyncio
import datetime
import json
from lxml import html
import requests
import slack
import time

__EVENT_LOOP = None
__EXPIRE_TIME = 0
__TITLE = ""
TIMER = None
ANNOUNCE_CHANNEL = "C6NQJSFRD"
TEST_CHANNEL = "GAE4LF0RH"
LOG_FILE = "/home/orion/mod_packt.log"

def log(*msg):
	log_message = ""
	with open(LOG_FILE, "a") as f:
		if type(msg) is tuple:
			for x in msg:
				log_message += str(x) + " "
			log_message += "\n"
		else:
			log_message = msg
		now = time.strftime("%Y-%m-%dT%H%M", time.gmtime())
		f.write(now + " " + log_message)

def countdown(sec):
	time = str(datetime.timedelta(seconds=sec))
	t = time.split(":")
	return t[0]+" hrs "+t[1]+" min"

def get_commands():
	return [{"command": "packt", "callback": say_packt_book},
			{"command": "packtbook", "callback": say_packt_book}]

def grab_book():
	global __EXPIRE_TIME, __TITLE
	if int(time.time()) >= __EXPIRE_TIME or __TITLE == "":
		HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0"}
		r = requests.request("GET", "https://www.packtpub.com/packt/offers/free-learning", data="", headers=HEADERS)
		page = r.content.decode("utf-8")
		tree = html.fromstring(page)
		r = tree.xpath('//span[@class="packt-js-countdown"]/@data-countdown-to')
		if r[0] == "":
			__TITLE = "No free book info published at this time." 
			__EXPIRE_TIME = int(time.time())+3600 # 1 hour.
			return
		__EXPIRE_TIME = int(r[0])
		#log("[DEBUG]", __EXPIRE_TIME, __TITLE)
		r = tree.xpath('//div[@class="dotd-title"]/h2/text()')
		__TITLE = r[0].strip()
#		r = tree.xpath('//noscript/img[@class="bookimage imagecache imagecache-dotd_main_image"]/@src')
#		image = r[0]
	return

def say_packt_book(args):
	global __TITLE, __EXPIRE_TIME
	print("[mod_packt] say_packt_book()", args)
	#p = await grab_book()
	grab_book()
	response = " ".join(["The current free Packt book is", '"'+__TITLE+'"', "\nThe offer will expire in", countdown(int(__EXPIRE_TIME-int(time.time()))),"\nYou can grab it here: https://www.packtpub.com/packt/offers/free-learning"])
	#log("[DEBUG]", response)
	return(response)
	#return "The packt and packtbook commands are not implemented."
	
def init():
	log("[DEBUG] [mod_packt] init()")
	slack.EVENT_LOOP.create_task(auto_announce())

async def auto_announce():
	while True:
		log("[DEBUG] auto_announce() Grabbing book data.")
		grab_book()
		wait = 300 # 5 minutes
		now = int(time.time())
		log("[DEBUG] wait is", wait, "time now is", now)
		if now > __EXPIRE_TIME:
			log("[DEBUG] Waiting for Packt update, sleeping", wait, "seconds @", now+wait)
			#TIMER = Timer(now+wait, auto_announce)
			await asyncio.sleep(wait)
			continue
		log("[DEBUG] announcing new book...")
		announcement = say_packt_book({})
		announce_task = slack.EVENT_LOOP.create_task(slack.send_msg(ANNOUNCE_CHANNEL, announcement))
		# sleep for 1 hour, there won't be a new book for AT LEAST that long! lol.
		wait = 3600
		asyncio.sleep(wait)
		if __EXPIRE_TIME-now > 300:
			wait = __EXPIRE_TIME-now # one hour
		else:
			wait = (__EXPIRE_TIME-now) + 60
		log("[DEBUG] Getting ready for the long sleep...", wait, "seconds")
		await asyncio.sleep(wait)

def main():
	#print(say_packt_book({}))
	slack.init()
	init()
	auto_announce()

if __name__ == "modules.mod_packt":
	init()

if __name__ == "__main__":
	main()
