import tkinter as tk
from tkinter import ttk
import os
import serial as sp
import threading
import datetime
import sys


class PyTerminal:
    def __init__(self, tkinter_object):
        if not isinstance(tkinter_object, tk.Tk):
            raise ValueError("Value must be a tkinter object!")
        self.tkinter_object = tkinter_object
        self.tkinter_object.title("SerialPort GUI Application")
        # self.tkinter_object.geometry('800x400')

        # Create a serialport obj here
        self.serialport = sp.Serial()
        self.timer_stop_evnet = threading.Event()
        self.timer_interval = 0.5  # seconds
        self.create_widget()

    def create_widget(self):
        self.frame_container1 = tk.Frame(self.tkinter_object)
        self.frame_container1.grid(column=0, row=0)
        self.frame_container2 = tk.Frame(self.tkinter_object)
        self.frame_container2.grid(column=1, row=1)

        self.combobox1_serialports = ttk.Combobox(self.frame_container1)
        self.combobox2_baudrates = ttk.Combobox(
            self.frame_container1,
            values=[
                "9600",
                "19200",
                "38400",
                "57600",
                "115200",
                "230400",
                "460800",
                "921600",
            ],
        )
        self.combobox2_baudrates.current(4)

        self.btn_serialport_connect = tk.Button(
            self.frame_container1,
            text="Connect",
            command=self.btn_serialport_connect_pressed_action,
        )
        self.btn_clear_text_area = tk.Button(
            self.frame_container1,
            text="Clear Console",
            command=self.btn_clear_text_area_pressed_action,
        )
        self.btn_scan_serialports = tk.Button(
            self.frame_container1,
            text="Scan",
            command=self.btn_scan_serialport_pressed_action,
        )

        self.text_field1 = tk.Entry(self.frame_container2)
        self.btn_transmitt_1 = tk.Button(
            self.frame_container2,
            text="Send",
            state="disabled",
            command=self.btn_transmitt_1_pressed_action,
        )
        self.text_field2 = tk.Entry(self.frame_container2)
        self.btn_transmitt_2 = tk.Button(
            self.frame_container2,
            text="Send",
            state="disabled",
            command=self.btn_transmitt_2_pressed_action,
        )

        self.textarea1 = tk.Text(self.tkinter_object, width=100, height=50)

        self.combobox1_serialports.grid(column=0, row=0)
        self.btn_serialport_connect.grid(column=1, row=0)
        self.btn_scan_serialports.grid(column=2, row=0)
        self.combobox2_baudrates.grid(column=3, row=0)
        self.btn_clear_text_area.grid(column=4, row=0)

        self.text_field1.grid(column=0, row=0)
        self.btn_transmitt_1.grid(column=1, row=0)
        self.text_field2.grid(column=0, row=1)
        self.btn_transmitt_2.grid(column=1, row=1)

        self.textarea1.grid(column=0, row=1)

        print("Creat Widget")

    def scan_serialports(self):
        if sys.platform.startswith('linux'):
            read = os.popen("python3 -m serial.tools.list_ports").read()
            print('linux platform')
        else:
            read = os.popen("python -m serial.tools.list_ports").read()            
            print('windows platform')
        self.serialport_list = read.split()
        self.serialport_count = 0
        for str in self.serialport_list:
            print(f"{self.serialport_count}:{str}")
            self.serialport_count += 1
        print("Scan all seriaports end")

    def update_combobox_value(self):
        self.combobox1_serialports.config(values=self.serialport_list)
        self.combobox1_serialports.current(0)

    def remove_combobox_value(self):
        self.combobox1_serialports["values"] = []
        self.combobox1_serialports.set("")

    def btn_scan_serialport_pressed_action(self):
        self.scan_serialports()
        if self.serialport_count > 0:
            self.update_combobox_value()
        else:
            self.remove_combobox_value()

    def btn_clear_text_area_pressed_action(self):
        self.textarea1.delete(1.0, "end")

    def serialport_open(self, port_name, baudrate):  # 8_n_1 as default
        self.serialport.port = port_name
        self.serialport.baudrate = baudrate
        self.serialport.bytesize = sp.EIGHTBITS
        self.serialport.parity = sp.PARITY_NONE
        self.serialport.stopbits = sp.STOPBITS_ONE
        self.serialport.open()
        if self.serialport.is_open:
            return True
        else:
            return False

    def serialport_close(self):
        if self.serialport.is_open:
            self.serialport.close()

    def serialport_sendbytes(self, data):
        if not isinstance(data, str):
            print("input not acceptable")
        else:
            if self.serialport.is_open and (data != ""):
                self.serialport.write(data.encode())

    def btn_serialport_connect_pressed_action(self):
        if self.btn_serialport_connect.cget("text") == "Connect":
            print(
                "PortName={0}:BaudRate={1}".format(
                    self.combobox1_serialports.get(),
                    int(self.combobox2_baudrates.get()),
                )
            )
            if (
                self.serialport_open(
                    self.combobox1_serialports.get(),
                    int(self.combobox2_baudrates.get()),
                )
                == True
            ):
                self.btn_serialport_connect.config(text="DisConnect")
                self.combobox1_serialports.config(state="disabled")
                self.combobox2_baudrates.config(state="disabled")
                self.btn_scan_serialports.config(state="disabled")
                self.btn_transmitt_1.config(state="active")
                self.btn_transmitt_2.config(state="active")
                print(f"Port {self.serialport.name} open successfully")
            else:
                print(f"Port {self.serialport.name} Open Failed")

        else:
            self.serialport_close()
            self.btn_serialport_connect.config(text="Connect")
            self.combobox1_serialports.config(state="active")
            self.combobox2_baudrates.config(state="active")
            self.btn_scan_serialports.config(state="active")
            self.btn_transmitt_1.config(state="disabled")
            self.btn_transmitt_2.config(state="disabled")
            print(f"Port {self.serialport.name} closed successfully")

    def btn_transmitt_1_pressed_action(self):
        self.serialport_sendbytes(self.text_field1.get())

    def btn_transmitt_2_pressed_action(self):
        self.serialport_sendbytes(self.text_field2.get())

    def timer_callback(self):
        if self.serialport.is_open and self.serialport.in_waiting > 0:
            data = self.serialport.read_all().decode("utf-8")
            self.textarea1.insert(tk.END, f"{datetime.datetime.now()} > {data}\n")

    def timer_start(self):
        threading.Thread(target=self.timer_thread).start()

    def timer_stop(self):
        self.timer_stop_evnet.set()

    def timer_thread(self):
        while not self.timer_stop_evnet.is_set():
            self.timer_callback()
            self.timer_stop_evnet.wait(self.timer_interval)


def main():
    root = tk.Tk()
    try:
        app = PyTerminal(root)
        app.timer_start()
        root.mainloop()
        app.serialport_close()
        app.timer_stop()
    except ValueError as e:
        print("Initialization Failed:", e)


if __name__ == "__main__":
    main()
