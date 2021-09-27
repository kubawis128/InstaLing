from tkinter import *
from tkinter import messagebox
import handler
import threading

autorunning = False

def init():
    global btn2
    global window
    window = Tk()
    window.title("Instaling bot")
    window.geometry('350x200')
    btn = Button(window, text="Init hander", command=initHandler)
    btn.grid(column=2, row=0)
    btn1 = Button(window, text="Solve task", command=solve)
    btn1.grid(column=3, row=0)
    btn2 = Button(window, text="Start Auto Mode", command=auto_solve)
    btn2.grid(column=4, row=0)
    btn3 = Button(window, text="Quit", command=exit)
    btn3.grid(column=5, row=0)
    window.mainloop()

def initHandler():
    handler.init()

def solve():
    handler.start()

def auto_solve():
    global btn2
    global autorunning
    if autorunning == True:
        autorunning = False
        btn2['text'] = "Start Auto Mode"
    else:
        autorunning = True
        btn2['text'] = "Stop Auto Mode"
    auto_loop()
def auto_loop():
    global autorunning
    if autorunning:
        handler.start()
        t = threading.Timer(5.0, auto_loop)
        t.start()
def exit():
    global window
    handler.exit()
    window.quit()
    return 0