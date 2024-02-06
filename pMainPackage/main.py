import tkinter as tk
from tkinter import ttk
from threading import Timer
import serial
import subprocess as sp
import os
from pprint import pprint
import threading
import time
import datetime
import find_serialports as fsp

#global serialport define
sp1 = serial.Serial()   
#main tk window init
main_window = tk.Tk()
main_window.title('SerialPort Test Program')
main_window.geometry('800x400')
# main_window.resizable(0,0)
textarea1 = tk.Text(main_window,width=100,height=50)
frame1 = tk.Frame(main_window)
btn1 = tk.Button(frame1, text='clear TextArea')
btn2 = tk.Button(frame1, text = 'Connect')
combobox1 = ttk.Combobox(frame1)
btn3 = tk.Button(frame1, text='SEND')
text_field = tk.Entry(frame1)
combobox1.grid(column=0,row=0)
btn1.grid(column=2,row=0)
btn2.grid(column=1,row=0)
btn3.grid(column=4,row=0)
text_field.grid(column=3,row=0)

    
#btn1 for clear console    
def btn1_clear_text():
    textarea1.delete(1.0,'end')

#btn2 for connect serial port
def btn2_pressed_action():
    if(btn2.cget('text') == 'Connect'):
        if(combobox1.current() >= 0):
            print('Combobox select text = {0}'.format(combobox1.get()))            
            sp1.baudrate = 115200
            sp1.stopbits = serial.STOPBITS_ONE
            sp1.bytesize = serial.EIGHTBITS
            sp1.parity = serial.PARITY_NONE
            sp1.port = combobox1.get()
            sp1.open()
            if(sp1.is_open == True):
                btn2.config(text= "disconnect")
                print('{0} open successfully'.format(sp1.name))
            else:
                print('{0} open Failed'.format(sp1.name))
    else: 
        btn2.config(text="Connect")
        if(sp1.is_open == True):
            sp1.close()
            print(f'{sp1.name}:closed')
def btn3_pressed_action():
    if((sp1.is_open)&(text_field.get()!='')):
        get_string = text_field.get()
        print('{0}'.format(get_string))
        sp1.write(get_string.encode())

#TODO: seperate from main py
#timer for scaning
stop_event = threading.Event()
# Set the timer duration in seconds
timer_interval = 0.5
def timer_callback():
    # print("Time's up!")
    if(sp1.is_open):
        if(sp1.in_waiting>0):
            textarea1.insert(tk.END,'{0}>{1}\n'.format(datetime.datetime.now(),sp1.read_all().decode('utf-8')))

def threading_timer(interval, stop_event):
    while not stop_event.is_set():
        timer = threading.Timer(interval, timer_callback)
        timer.start()
        timer.join()

#MAIN Function
def main():
    serialport_list = fsp.find_serialport()
    btn2.config(command=btn2_pressed_action)
    btn1.config(command=btn1_clear_text)
    btn3.config(command=btn3_pressed_action)
    combobox1.config(values=serialport_list)
    if(serialport_list.count != 0):
        combobox1.current(0)
    #widgets layout settings
    frame1.pack()
    textarea1.pack()
    main_window.mainloop()
    # Wait for the timer thread to complete
    stop_event.set()
    # Wait for the timer thread to complete
    timer_thread.join()
    #close serial port
    if(sp1.is_open == True):
        sp1.close()

if __name__ == '__main__':   
# Start the threading timer
    timer_thread = threading.Thread(target=threading_timer,args=(timer_interval,stop_event))
    timer_thread.start()
    main()
    print('End of program')