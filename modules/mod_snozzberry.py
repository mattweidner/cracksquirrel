# File: mod_snozzberry.py
# Date: 2018-08-03
# Author: Matt Weidner <matt.weidner@gmail.com>
# Description: Snozzberry module
#
import json
import random
import time

responses = [ "Squirrel’s don’t eat snozzberries, you moron. Unless they're on crack.",
              "All I know about snozzberries is they taste like snozzberries.",
              "Snozzberry Pi you say? Yum.",
              "https://preview.ibb.co/miT7Ue/snozzberry_cat.jpg",
              "Have you tasted a snozzberry? Nasty...",
              "Do you know where I can get some?",
              "Who's your supplier? Let me guess... @miller1371?",
              "Who's your supplier? Let me guess... @Ryan Hopkins?",
              "https://i.imgflip.com/2h5878.jpg",
              "Snozzberries... You can't eat just one!\nhttps://image.ibb.co/nr8dcz/square_Snozzberry.jpg"

        ]



def get_commands():
    return [{"command": "snozzberry", "callback": say_snozz},
            {"command": "snozzberries", "callback": say_snozz},]

def say_snozz(args):
    return random.choice(responses)


def init():
    print("[DEBUG] [mod_snozzberry.py] init()")

def main():
	print(say_snozz("arg"))

if __name__ == "modules.mod_snozzberry":
    init()

if __name__ == "__main__":
    main()
