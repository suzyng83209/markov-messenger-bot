import fbchat
from MarkovModel import MarkovModel
import urllib2
import time
import random
# subclass fbchat.Client and override required methods


class EchoBot(fbchat.Client):

    def __init__(self, email, password, debug=True, user_agent=None):
        fbchat.Client.__init__(self, email, password, debug, user_agent)
        self.m = MarkovModel()
        self.enabled = False

    def on_message(self, mid, author_id, author_name, message, metadata):
        self.markAsDelivered(author_id, mid)  # mark delivered
        self.markAsRead(author_id)  # mark read

        # if str(author_id) == str(self.uid):
        #
        #     if message.body == 'Start':
        #         self.enabled = True
        #     elif message.body == 'Stop':
        #         self.enabled = False
        #         print self.enabled

        # if you are not the author, echo
        domain = "https://senderbot.herokuapp.com/send~"
        # print self.enabled
        if str(author_id) != str(self.uid) and self.enabled:
            # self.send(author_id, message)
            time.sleep(random.uniform(1, 5))

            text=self.m.generate()
            text='%20'.join(text.split())
            urllib2.urlopen(domain + text + "~" + str(author_id))
            # urllib2.urlopen("https://senderbot.herokuapp.com/send~LOL~1135881167")

bot = EchoBot("waterloogoosehonk@gmail.com'", "HiIAmGoose101")
bot.listen()
