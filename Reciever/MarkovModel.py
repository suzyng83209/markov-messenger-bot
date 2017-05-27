import markovify
import os.path
from os import listdir
from os.path import isfile, join


class MarkovModel(object):
    models = []
    overallModel = ""

    def __init__(self):
        self.loadText()

    def loadText(self):
        path = 'Reciever/Data/'
        files = [f for f in listdir(path)
                 if isfile(join(path, f))]
        for f in files:
            with open("Reciever/DATA/" + f) as fi:
                text = fi.read()
            # makes models
            self.models.append(markovify.Text(text))
        self.overallModel = markovify.combine(self.models)

    def generate(self):
        msg = None
        try:
            msg = self.overallModel.make_sentence_with_start("i")
        except:
            False

        # print(msg)

        if (msg == None):
            msg = self.overallModel.make_sentence()

        if (msg != None):
            return msg
        else:
            return "RAD"
