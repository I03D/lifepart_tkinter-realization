import win32gui, win32con
program = win32gui.GetForegroundWindow()
win32gui.ShowWindow(program, win32con.SW_HIDE)
import win32api

import os

import configparser

import ctypes
import ctypes.wintypes as w

import sys

import threading

import subprocess
import time
from math import floor

from pystray import MenuItem as item
import pystray
from PIL import Image, ImageTk

import tkinter as tk

# subprocess.run(["python", "Blinker45.pyw"])
subprocess.run(["Blinker45.exe"])

# os.system('cls')


config = configparser.ConfigParser()
config.read('config.ini')

root = tk.Tk()
root.geometry("460x170")
T = tk.Text(root, height = 170, width = 460, bg = config['settings']['background_color'], fg = config['settings']['foreground_color'])
T.pack(side="top", fill="both", expand=True)

def toggle_window():
    global sh
    if sh:
        sh = False
        # win32gui.ShowWindow(program , win32con.SW_SHOW)
        root.deiconify()
    else:
        sh = True
        # win32gui.ShowWindow(program , win32con.SW_HIDE)
        root.withdraw()
        
def hiding_by_close():
    sh = True
        
        

sh = config['settings']['show_cmd']

if sh == "False":
    sh = False
else:
    sh = True
    
toggle_window()

def quit_window():
    config['settings']['show_cmd'] = str(not sh)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    win32gui.SendMessage(program, win32con.WM_CLOSE)


def showIcon():
    image=Image.open("flower.png")
    menu=(item('Показать/скрыть', toggle_window), item('Выход', quit_window))
    icon=pystray.Icon("name", image, "LifePart", menu)
    icon.run()

x = threading.Thread(target=showIcon, args=())
x.start()




# print("~ Мигалка ~")
# print("Эта программа напоминает сделать 15-минутный перерыв после 45 минут работы и смотреть вдаль каждые 5 минут.")
# print("(Чтобы скрыть окно, нажмите Windows+Вниз)")

process_name='LogonUI.exe'
callall='TASKLIST'
locked = False

# T.insert("end", "Время пошло.")





root.protocol("WM_DELETE_WINDOW", toggle_window)

T.tag_configure("center", justify='center')
T.insert("end", "~ Мигалка ~\n")
T.tag_add("center", "1.0", "end")


T.insert("end", "Эта программа напоминает сделать 15-минутный перерыв\n после 45 минут работы и смотреть вдаль каждые 5 минут.\n(Чтобы скрыть окно, нажмите Windows+Вниз или Alt+F4)\n")

   
small_timer = 0
big_timer = 0

big_timer_start = floor(time.time())
small_timer_start = big_timer_start
def SEND():
    global timer_start
    
    global big_timer
    global small_timer
    
    global big_timer_start
    global small_timer_start
    
    global locked
    # if not locked:
        # timer += 1
    # print("debug: timer = " + str(timer))
    # T.insert("end", "debug: timer = "+str(timer)+"\n")
    # T.insert("end", "debug: time.time() = " + str(floor(time.time())) + "\n")
    
    outputall=subprocess.check_output(callall,shell=False)
    outputstringall=str(outputall)
    if process_name in outputstringall:
        if not locked:
            # print("Сессия заблокирована, сбрасываем время.\n")
            T.insert("end", "Сессия заблокирована, сбрасываем время.\n")
            big_timer_start = floor(time.time())
            small_timer_start = floor(time.time())
        locked = True
    else:
        if locked:
            # print("Сессия разблокирована, время пошло.\n")
            T.insert("end", "Сессия разблокирована, время пошло.\n")
            big_timer_start = floor(time.time())
            T.insert("end", "debug: big_timer_start = " + str(big_timer_start)+"\n")
            small_timer_start = floor(time.time())
            T.insert("end", "debug: small_timer_start = " + str(small_timer_start)+"\n")
            locked = False
        
        timestamp = floor(time.time())
        big_timer = timestamp - big_timer_start
        small_timer = timestamp - small_timer_start

        # print("debug: timestamp = " + str(timestamp)+"\n")
        # print("debug: big_timer = " + str(big_timer)+"\n")
        # print("debug: small_timer = " + str(small_timer)+"\n")
        # T.insert("end", "debug: big_timer = " + str(big_timer)+"\n")
        if small_timer > 300:
            # print("Прошло " + str(floor(timer/60)) + " минут.")
            T.insert("end", "Прошло " + str(floor(big_timer/60)) + " минут.\n")
            small_timer = 0
            small_timer_start = timestamp
            if big_timer >= 2700:
                # subprocess.run(["python", "Blinker45.pyw"])
                subprocess.run(["Blinker45.exe"])
                if big_timer < 3000:
                    # print("Пора сделать 15-минутный перерыв.\n")
                    T.insert("end", "Пора сделать 15-минутный перерыв.\n")
                else:
                    # print("Пора сделать хотя бы 15-минутный перерыв.\n")
                    T.insert("end", "Пора сделать хотя бы 15-минутный перерыв.\n")
                # print("(Windows+L заблокирует сессию и сбросит таймер в течение "+config['settings']['update_frequency']/100+" секунд)\n")
                T.insert("end", "(Windows+L заблокирует сессию и сбросит таймер в течение 5 минут)\n")
            else:
                # subprocess.run(["python", "Blinker5.pyw"])
                subprocess.run(["Blinker5.exe"])
    T.see("end")
    root.after(config['settings']['update_frequency'], SEND)


SEND()
tk.mainloop()

