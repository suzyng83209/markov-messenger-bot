import fbchat
from MarkovModel import MarkovModel
import urllib2
import time
import random
import json
# subclass fbchat.Client and override required methods


class EchoBot(fbchat.Client):
    m = MarkovModel()
    stores ={"sears":"www.sears.ca", "tunnelbear":"www.tunnelbear.com"}

    def __init__(self, email, password, debug=True, user_agent=None):
        fbchat.Client.__init__(self, email, password, debug, user_agent)

    def on_message(self, mid, author_id, author_name, message, metadata):
        self.markAsDelivered(author_id, mid)  # mark delivered
        self.markAsRead(author_id)  # mark read

        domain = "https://senderbot.herokuapp.com/send~"
        message=message.lower()
        j = urllib2.urlopen("https://toggleserver.herokuapp.com/get")
        jsonResponse = json.load(j)
        jsonData = jsonResponse["botOn"]

        if not jsonData:
            return

        if str(author_id) != str(self.uid):
            # if message == '/shopping' or message.index("shopping")>=0:
            #     urllib2.urlopen(domain + "www.sears.ca" + "~" + str(author_id))
            #     return
            # elif message ==

            for k in self.stores.keys():
                if k in message:
                    urllib2.urlopen(domain + self.stores[k] + "~" + str(author_id))
                    return



            text=self.m.generate()
            text='%20'.join(text.split())
            time.sleep(random.uniform(1, len(text)/30))
            urllib2.urlopen(domain + text + "~" + str(author_id))
            # urllib2.urlopen("https://senderbot.herokuapp.com/send~LOL~1135881167")

bot = EchoBot("waterloogoosehonk@gmail.com'", "HiIAmGoose101")
bot.listen()
