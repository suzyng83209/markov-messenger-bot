import applicationhandler
import mousehandler

def run (c):
    if len (c)==1:
        if c[0] in set(tuple(["click"])):
            mousthandler.Click()
            return True
        return False

    elif len(c)>1:
        if c[0] in set(tuple(["open", "app","application"])):
            applicationhandler.OpenApp(c[1])
            return True
        # elif c[0] in set(tuple(["cursor", "mouse"])):
        #     val=5
        #     if c[1]=="up":
        #         mousehandler.Move(0,val)
        #     elif c[1]=="down":
        #         mousehandler.Move(0,-val)
        #     elif c[1]=="left":
        #         mousehandler.Move(val,0)
        #     elif c[1]=="right":
        #         mousehandler.Move(-val,0)
        #     else:
        #         return False
        #     return True
        elif c[0] in set(tuple(["scroll"])):
            if c[1]=="up":
                mousehandler.Scroll(1)
            if c[1]=="down":
                mousehandler.Scroll(-1)
            else:
                return False
            return True
        elif c[0]=="double" and c[1]=="click":
            mousehandler.DoubleClick()
            return True

    return False
