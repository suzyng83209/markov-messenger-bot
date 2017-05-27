import Config
import fbchat

class TestBot(fbchat.Client):

    def __init__(self, email, password, debug=True, user_agent=None):
        fbchat.Client.__init__(self, email, password, debug, user_agent)

    def on_message(self, mid, author_id, author_name, message, metadata):
        self.markAsDelivered(author_id, mid)
        self.markAsRead(author_id)

        print("%s said: %s"%(author_id, message))

        if str(author_id) != str(self.uid):
            self.send(author_id, message)

bot = TestBot(Config.USER, Config.PASSWORD)
bot.listen()