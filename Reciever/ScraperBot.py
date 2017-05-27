import fbchat
# subclass fbchat.Client and override required methods


class ScraperBot():
    client = fbchat.Client("waterloogoosehonk@gmail.com'", "HiIAmGoose101")

    # returns a giant string of all messages
    def getScrapedData(self, name):
        friend = self.client.getUsers(name)[0]
        last_messages = self.client.getThreadInfo(
            friend.uid, last_n=50)
        last_messages.reverse()  # messages come in reversed order

        return '.'.join([last_messages[i].body for i in range(1, len(last_messages))])

ScraperBot = ScraperBot()
print ScraperBot.getScrapedData("Susan")
