import os.path
from os import listdir
from os.path import isfile, join
import subprocess


class MarkovModel(object):
    models = []
    overallModel = ""

    def generate(self):
        return subprocess.check_output("python ../run.py")

if __name__ == "__main__":
    a = MarkovModel()

    print a.generate()
