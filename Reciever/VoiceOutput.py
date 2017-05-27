import subprocess

def Say(text):
    try:
        subprocess.call(["say",text])
    except:
        return