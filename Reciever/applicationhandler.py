import subprocess
import VoiceOutput


def __init__ ():
    this.hi=1

def OpenApp(s):
    try:
        o=subprocess.check_output(["open","-a",s])
        if o.startswith("Unable"):
            VoiceOutput.Say("Unable to open "+str(s))


    except:
        print "application open failed"
        VoiceOutput.Say("Unable to open "+str(s))
        return
