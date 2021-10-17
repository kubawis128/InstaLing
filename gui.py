from tkinter import ttk
import tkinter as tk
import handler
import threading
from ttkthemes import ThemedTk
import config

autorunning = False

def init():
    global btn2
    global window
    global lang
    window = ThemedTk(theme='arc')
    window.title("Instaling bot")
    window.geometry('350x200')
    lang = tk.StringVar(window)
    lang.set("de")
    x = threading.Thread(target=initHandler)
    #s = ttk.Style()
    #s.configure('TButton', foreground='white')
    btn = ttk.Button(window, text="Init hander", command=x.start)
    btn.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
    btn1 = ttk.Button(window, text="Solve task", command=solve)
    btn1.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    btn2 = ttk.Button(window, text="Start Auto Mode", command=auto_solve)
    btn2.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    btn3 = ttk.Button(window, text="Quit", command=exit)
    btn3.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
    list = ttk.OptionMenu(window, lang, "de","de", "en",command=changeLang)
    list.place(relx=0.1, rely=0.1, anchor=tk.CENTER)
    window.mainloop()
    

def initHandler():
    handler.init()
def changeLang(hel = 0):
    global lang
    config.saveConf('translator','to',lang.get())
def solve():
    handler.start()

def auto_solve():
    global btn2
    global t 
    global autorunning
    if autorunning == True:
        autorunning = False
        try:
            t.cancel()
        except:
            pass
        btn2['text'] = "Start Auto Mode"
    else:
        autorunning = True
        btn2['text'] = "Stop Auto Mode"
    auto_loop()
def auto_loop():
    global t 
    global autorunning
    if autorunning:
        handler.start()
        t = threading.Timer(int(config.getConf('automode','sleep')), auto_loop)
        t.start()
def exit():
    global window
    handler.exit()
    window.quit()
    return 0