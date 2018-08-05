# File: secretsquirrel2.py
# Date: 2018-08-03
# Author: Matt Weidner <matt.weidner@gmail.com>
# Description: Secret Squirrel Slackbot
#
import asyncio
import importlib
import json
import pathlib
import signal
import slack

commands = []

def load_modules():
    modules_path = pathlib.Path("modules/")
    for module in modules_path.iterdir():
        if module.is_dir():
            continue
        if str(module.name).startswith("mod_"):
            module_name = module.name
            module_name = module_name.split(".")[0]
#           print("[DEBUG] Loading module", "modules."+module_name)
            m = importlib.import_module("modules."+module_name, "modules.subpkg")
            if not m is None:
                cmds = m.get_commands()
                #print("[DEBUG]", cmds)
                if not cmds is None:
                    commands.append({"module": m, "command_list": cmds})
#       else:
#           print("[DEBUG] Skipping", module)
    importlib.invalidate_caches()

def test_modules():
    for m in commands:
        #print("[DEBUG]", m)
        for c in m["command_list"]:
            #print("[DEBUG]", c)
            r = c["callback"]([c["command"]])
            print("[DEBUG] test_modules()    [+] module says", r)

async def bot_callback(message):
    global commands
    #print("[DEBUG] message recvd:", message)
    if message is None:
        return
    attention_types = ["goodbye", "hello", "message"]
    try:
        msg = json.loads(message)
    except Exception as e:
        print("[!] bot_callback() Unable to unmarshall json", e)
        print("[!]     ", message)
        return
    if not "type" in msg.keys():
        return
    if not msg["type"] in attention_types:
        return
    if msg["type"] == "goodbye":
        slack.terminate("SIGTERM")
        return
    if msg["type"] == "hello":
        print("[+] Ready.")
    if msg["type"] == "message":
        if "message" in msg.keys():
            if "edited" in msg["message"]:
                chan = msg["channel"]
                msg = msg["message"]
                if msg["user"] == slack.SELF["id"]:
                    return
                msg["channel"] = chan
        try:
            print("C:", msg["channel"], "U:", msg["user"])
            print("[DEBUG]", msg["text"])
        except KeyError:
            print("[DEBUG] bot_callback() KeyError:", msg)
            return
        if "@"+slack.SELF["name"] in msg["text"] or "@"+slack.SELF["id"] in msg["text"]:
            #print("[DEBUG] bot_callback() detected self.")
            #print("[DEBUG] evaluating message:", msg)
            matched = False
            for module in commands:
                for c in module["command_list"]:
                    #print("    [DEBUG]", c)
                    if c["command"] in msg["text"]:
                        #print("[DEBUG] bot_callback() matched command", c["command"])
                        matched = True
                        mod_cmd = c["callback"]
                        try:
                            response = mod_cmd(msg)
                        except Exception as e:
                            print("[!] Error calling module function", mod_cmd)
                            print("[!]", e)
                            return
                        #print("[DEBUG] bot_callback() module response:", response)
                        await slack.send_msg(msg["channel"], response)
                #print("[DEBUG] bot_callback() exiting for loop.")
            if not matched:
                # No command was matched to the input message.
                # Tell the user what commands are available.
                available_commands = []
                for module in commands:
                    for c in module["command_list"]:
                        if not c["command"] in available_commands:
                            available_commands.append(c["command"])
                await slack.send_msg(msg["channel"], "You talkin to me? I have no idea what you just said.\nBetter say it like this next time:\n`@cracksquirrel <cmd>`\nHere are the commands I know about:\n```"+str(available_commands)+"```\nIf I can't do what you want me to, talk to that lazy, good for nothing Matt Weidner.")

def test_slack():
    if slack.connect(bot_callback) == False:
        print("[!] test_slack() Error connecting to Slack")

def main():
#   test_modules()
#   test_slack()
    print("Loading modules...")
    load_modules()
    print("Connecting...")
    if slack.connect(bot_callback) == False:
        print("[!] main() Error connecting to Slack")
    print("Terminated.")

if __name__ == "__main__":
    main()
