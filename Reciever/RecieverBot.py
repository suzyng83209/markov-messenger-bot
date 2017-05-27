import fbchat
from MarkovModel import MarkovModel
import urllib2
import time
import random
import json
import requests
import Handler
# subclass fbchat.Client and override required methods


class EchoBot(fbchat.Client):
    #TODO
    m = MarkovModel()
    stores ={"sears":"www.sears.ca", "tunnelbear":"www.tunnelbear.com", "capital one": "www.capitalone.ca", "wish":"www.wish.com","td" :"www.tdcanadatrust.com/products-services/banking/index-banking.jsp","mlh":"https://mlh.io/","bell":"http://www.bell.ca/"}

    def __init__(self, email, password, debug=True, user_agent=None):
        fbchat.Client.__init__(self, email, password, debug, user_agent)

    def on_message(self, mid, author_id, author_name, message, metadata):
        self.markAsDelivered(author_id, mid)  # mark delivered
        self.markAsRead(author_id)  # mark read

        domain = "https://senderbot.herokuapp.com/send~"
        message=message.lower()
        tokens = message.split()
        j = urllib2.urlopen("https://toggleserver.herokuapp.com/get")
        jsonResponse = json.load(j)
        jsonData = jsonResponse["botOn"]

        if not jsonData:
            return

        if str(author_id) != str(self.uid):

            if Handler.run(tokens):
                return

            for s in self.stores.keys():
                if s in message:
                    p = {"command": "send","text": self.stores[s],"id": str(author_id)}
                    r = requests.post("https://senderbot.herokuapp.com", json = p)
                    return


            if "buy" in tokens and tokens.index("buy")+1<len(tokens):
                p = {"command": "send","text": "http://www.sears.ca/en/search?q="+tokens[tokens.index("buy")+1],"id": str(author_id)}
                r = requests.post("https://senderbot.herokuapp.com", json = p)
                return

            # TODO
            text=self.m.generate()
            # time.sleep(random.uniform(1, len(text)/50))
            p = {"command": "send","text": text,"id": str(author_id)}
            r = requests.post("https://senderbot.herokuapp.com", json = p)

bot = EchoBot("waterloogoosehonk@gmail.com'", "HiIAmGoose101")
bot.listen()
