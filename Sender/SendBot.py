import fbchat as fbchat
import Config

# client = fbchat.Client(Config.user, Config.password)


class EchoBot(fbchat.Client):

    def __init__(self, email, password, debug=True, user_agent=None):
        fbchat.Client.__init__(self, email, password, debug, user_agent)

    def on_message(self, mid, author_id, author_name, message, metadata):
        self.markAsDelivered(author_id, mid)  # mark delivered
        self.markAsRead(author_id)  # mark read

        print("%s said: %s" % (author_id, message))

        # if you are not the author, echo
        if str(author_id) != str(self.uid):
            self.send(author_id, message)

bot = EchoBot(Config.user, Config.password)
bot.listen()
