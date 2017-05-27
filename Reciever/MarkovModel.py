import os
import pickle

import subprocess

import settings
import tools

class MarkovModel(object):
    def generate(self):
        return subprocess.check_output("python ../run.py")