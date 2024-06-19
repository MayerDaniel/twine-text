import imessage
import re
import os
import sys
import urllib.request
from bs4 import BeautifulSoup
import json
from pprint import pprint


MESSAGE_CONTENT = 0
GUID = 1


class Adventure():
    def __init__(self, json_path):
        t = json.load(open(json_path, 'r'))
        self.twine = t['passages']
        for p in self.twine:
            p['pid'] = p['pid'] - 1
            for l in p['links']:
                l['destination']['pid'] = l['destination']['pid'] - 1
        self.pid_map = {}
        self.react_map = ["Loved", "Liked", "Disliked", "Laughed", "Emphasized", "Questioned"]
        self.react_emoji_map = ["️💙", "👍", "👎", "😂", "❗", "❓"]
    def send_message(self, string, guid):
        string = string.replace("'", "")
        string = string.replace('"', '')
        if ";+;chat" not in guid:
            body = """
            osascript -e 'tell application "Messages"
              set targetBuddy to "%s"
              set targetService to id of 1st account whose service type = iMessage
              set textMessage to "%s"
              set theBuddy to participant targetBuddy of account id targetService
              send textMessage to theBuddy
            end tell' """ % (guid, string)
        else:
            body = """
            osascript -e 'tell application "Messages"
              set myid to "%s"
              set textMessage to "%s"
              set theBuddy to a reference to chat id myid
              send textMessage to theBuddy
            end tell' """ % (guid, string)
        print(body)
        os.system(body)

    def convert_to_imessage(self, pid):
        out = self.twine[pid]['text']
        if len(self.twine[pid]['links']) > len(self.react_map):
            print("Too many links in this passage, exiting")
            sys.exit(1)
        for i,link in enumerate(self.twine[pid]['links']):
            out = out.replace("[[" + link['text'] + "]]", 
                                self.react_emoji_map[i] + " - " + link['text'])
        return out
    
    def start_adventure(self, guid):
        # add guid to pid_map and send first message
        self.pid_map[guid] = 0
        self.send_message("You have been invited to participate in an adventure. Use your imessage reacts to make decisions. Choose deliberately, you cannot choose again. Only onwards.", guid)
        self.send_message(self.convert_to_imessage(0), guid)

    def take_action(self, guid, option):
        # update the guid map and send the next message
        guid = guid
        self.pid_map[guid] = self.twine[self.pid_map[guid]]['links'][option]['destination']['pid']
        self.send_message(self.convert_to_imessage(self.pid_map[guid]), guid)

    def read(self, message):
        flag = False
        guid = message[GUID]
        for pid in self.pid_map:
            if pid in guid and guid != pid:
                guid = pid
        if guid in self.pid_map and message[MESSAGE_CONTENT]:
            text = message[MESSAGE_CONTENT].text
            date = message[MESSAGE_CONTENT].date
            command = text.split(" ")
            if(command[0] in self.react_map):
                option = command[0]
                self.take_action(guid, self.react_map.index(option))
            
            