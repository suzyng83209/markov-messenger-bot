import pyautogui

def Move(x,y):
    xSize,ySize = pyautogui.size()
    
    if x<0 or y<0 or x>xSize or y>ySize:
        return False
    pyautogui.moveTo(x,y,0.25)
    
    
    
def Click():
    pyautogui.click()
    
def DoubleClick():
    pyautogui.doubleClick(interval=0.2)

        
def Scroll(d):# 1 =down, -1 =up
    pyautogui.scroll(-10*d)
