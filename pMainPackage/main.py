import time
import tkinter as tk
from tkinter import ttk
import os
import serial as sp
import serial.tools.list_ports
import threading
import datetime
import sys


class PyTerminal:
    def __init__(self, tkinter_object):
        if not isinstance(tkinter_object, tk.Tk):
            raise ValueError("Value must be a tkinter object!")
        self.tkinter_object = tkinter_object
        self.tkinter_object.title("SerialPort GUI Application")
        self.tkinter_object.resizable(False, False)
        # self.tkinter_object.geometry('800x400')

        # Create a serialport obj here
        self.serialport = sp.Serial()
        self.timer_stop_event = threading.Event()
        self.timer_interval = 0.01  # seconds
        self.create_widget()

    def create_widget(self):
        self.frame_container1 = tk.Frame(self.tkinter_object)
        self.frame_container2 = tk.Frame(self.tkinter_object)

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

        self.combobox3_CRLR = ttk.Combobox(
            self.frame_container2,
            values=["NONE", "+ LF", "+ CR", "+ LFCR", "+ CRLF", "+LF * +CR"],
        )
        self.combobox3_CRLR.current(0)

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
        self.text_field3 = tk.Entry(self.frame_container2)
        self.btn_transmitt_3 = tk.Button(
            self.frame_container2,
            text="Send",
            state="disabled",
            command=self.btn_transmitt_3_pressed_action,
        )
        self.text_field4 = tk.Entry(self.frame_container2)
        self.btn_transmitt_4 = tk.Button(
            self.frame_container2,
            text="Send",
            state="disabled",
            command=self.btn_transmitt_4_pressed_action,
        )
        self.text_field5 = tk.Entry(self.frame_container2)
        self.btn_transmitt_5 = tk.Button(
            self.frame_container2,
            text="Send",
            state="disabled",
            command=self.btn_transmitt_5_pressed_action,
        )
        self.text_field_for_hex = tk.Entry(self.frame_container2)
        self.btn_transmitt_hex = tk.Button(
            self.frame_container2,
            text="Send",
            state="disabled",
            command=self.btn_transmitt_hex_pressed_action,
        )

        self.checkbox_timeline_mode_value = tk.BooleanVar()
        self.checkbox_timeline_mode = tk.Checkbutton(
            self.frame_container2,
            text="Time Line Mode",
            variable=self.checkbox_timeline_mode_value,
            command=self.checkbox_timeline_mode_pressed_action,
        )

        self.checkbox_scoll2bottom_value = tk.BooleanVar()
        self.checkbox_scoll2bottom = tk.Checkbutton(
            self.frame_container2,
            text="Scoll Bottom",
            variable=self.checkbox_scoll2bottom_value,
        )
        self.checkbox_scoll2bottom.select()  # set default mode on ->self.checkbox_scoll2bottom_value=1

        self.checkbox_hex_mode_value = tk.BooleanVar()
        self.checkbox_hex_mode = tk.Checkbutton(
            self.frame_container2,
            text="Hex Mode",
            variable=self.checkbox_hex_mode_value,
            command=self.checkbox_hex_mode_selected_action,
        )

        self.checkbox_treat_cr_as_lf_value = tk.BooleanVar()
        self.checkbox_treat_cr_as_lf = tk.Checkbutton(
            self.frame_container2,
            text="Treat CR as LF",
            variable=self.checkbox_treat_cr_as_lf_value,
        )
        self.checkbox_treat_cr_as_lf.select()  # set default CR = LF mode

        self.textarea1 = tk.Text(self.tkinter_object, width=77, height=25)
        self.textarea1_scrollbar = tk.Scrollbar(self.tkinter_object)
        self.textarea1.config(
            yscrollcommand=self.textarea1_scrollbar.set, state="disabled"
        )

        self.label1 = tk.Label(self.frame_container2, text="Hex input:")
        # frame 1  grid setup
        self.combobox1_serialports.grid(column=0, row=0)
        self.btn_serialport_connect.grid(column=1, row=0)
        self.btn_scan_serialports.grid(column=2, row=0)
        self.combobox2_baudrates.grid(column=3, row=0)
        self.btn_clear_text_area.grid(column=4, row=0)
        # frame 2 grid setup
        self.text_field1.grid(column=0, row=0)
        self.btn_transmitt_1.grid(column=1, row=0)
        self.text_field2.grid(column=0, row=1)
        self.btn_transmitt_2.grid(column=1, row=1)
        self.text_field3.grid(column=0, row=2)
        self.btn_transmitt_3.grid(column=1, row=2)
        self.text_field4.grid(column=0, row=3)
        self.btn_transmitt_4.grid(column=1, row=3)
        self.text_field5.grid(column=0, row=4)
        self.btn_transmitt_5.grid(column=1, row=4)
        self.label1.grid(column=0, row=5)
        self.text_field_for_hex.grid(column=0, row=6)
        self.btn_transmitt_hex.grid(column=1, row=6)
        self.checkbox_timeline_mode.grid(column=0, row=7, sticky=tk.W)
        self.checkbox_scoll2bottom.grid(column=0, row=8, sticky=tk.W)
        self.combobox3_CRLR.grid(column=0, row=9, sticky=tk.W)
        self.checkbox_hex_mode.grid(column=0, row=10, sticky=tk.W)
        self.checkbox_treat_cr_as_lf.grid(column=0, row=11, sticky=tk.W)

        # top layer grid setup
        self.frame_container1.grid(column=0, row=0)
        self.frame_container2.grid(column=2, row=1)
        self.textarea1.grid(column=0, row=1)
        self.textarea1_scrollbar.grid(column=1, row=1, sticky=tk.N + tk.S + tk.W)

        print("Creat Widget")

    def scan_serialports(self):
        self.portlist = serial.tools.list_ports.comports()
        self.portlist_name = [port.device for port in self.portlist]
        i = 0
        print(f"Find {len(self.portlist)} ports")
        for port, desc, hwid in self.portlist:
            print(f"{i}:{port},{desc},{hwid}")
            i += 1
        # if sys.platform.startswith("linux"):
        #     read = os.popen("python3 -m serial.tools.list_ports").read()
        #     print("linux platform")
        # else:
        #     read = os.popen("python -m serial.tools.list_ports").read()
        #     print("windows platform")
        # self.serialport_list = read.split()
        # self.serialport_count = 0
        # for str in self.serialport_list:
        #     print(f"{self.serialport_count}:{str}")
        #     self.serialport_count += 1

    def update_combobox_value(self):
        self.combobox1_serialports.config(values=self.portlist_name)
        self.combobox1_serialports.current(0)

    def remove_combobox_value(self):
        self.combobox1_serialports["values"] = []
        self.combobox1_serialports.set("")

    def btn_scan_serialport_pressed_action(self):
        self.scan_serialports()
        if len(self.portlist) > 0:
            self.update_combobox_value()
        else:
            self.remove_combobox_value()

    def btn_clear_text_area_pressed_action(self):
        self.textarea1.config(state="normal")
        self.textarea1.delete(1.0, "end")
        self.textarea1.config(state="disabled")

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

    def make_string(self, combobox_text, target_string):
        if combobox_text == "+ LF":
            return target_string + "\n"
        elif combobox_text == "+ CR":
            return target_string + "\r"
        elif combobox_text == "+ LFCR":
            return target_string + "\n\r"
        elif combobox_text == "+ CRLF":
            return target_string + "\r\n"
        elif combobox_text == "+LF * +CR":
            return "\n" + target_string + "\r"
        else:
            return None

    def serialport_sendbytes_from_String(self, data):
        if not isinstance(data, str):
            print("input not acceptable")
        else:
            if self.serialport.is_open and (data != ""):
                if not self.combobox3_CRLR.get() == "NONE":
                    self.serialport.write(
                        self.make_string(self.combobox3_CRLR.get(), data).encode()
                    )
                else:
                    self.serialport.write(data.encode())

    def btn_serialport_connect_pressed_action(self):
        if self.btn_serialport_connect.cget("text") == "Connect":
            if self.combobox1_serialports.get() == "":
                print("Error: No valid port")
                return
            else:
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
                self.hex_mode_object_control()
                print(f"Port {self.serialport.name} open successfully")
            else:
                print(f"Port {self.serialport.name} Open Failed")

        else:
            self.serialport_close()
            self.btn_serialport_connect.config(text="Connect")
            self.combobox1_serialports.config(state="active")
            self.combobox2_baudrates.config(state="active")
            self.btn_scan_serialports.config(state="active")
            self.hex_mode_object_control()
            print(f"Port {self.serialport.name} closed successfully")

    def hex_mode_object_control(self):
        if self.serialport.is_open:
            if self.checkbox_hex_mode_value.get() == True:
                self.btn_transmitt_hex.config(state="active")
                self.btn_transmitt_1.config(state="disabled")
                self.btn_transmitt_2.config(state="disabled")
                self.btn_transmitt_3.config(state="disabled")
                self.btn_transmitt_4.config(state="disabled")
                self.btn_transmitt_5.config(state="disabled")
            else:
                self.btn_transmitt_hex.config(state="disabled")
                self.btn_transmitt_1.config(state="active")
                self.btn_transmitt_2.config(state="active")
                self.btn_transmitt_3.config(state="active")
                self.btn_transmitt_4.config(state="active")
                self.btn_transmitt_5.config(state="active")

    def btn_transmitt_1_pressed_action(self):
        self.serialport_sendbytes_from_String(self.text_field1.get())

    def btn_transmitt_2_pressed_action(self):
        self.serialport_sendbytes_from_String(self.text_field2.get())

    def btn_transmitt_3_pressed_action(self):
        self.serialport_sendbytes_from_String(self.text_field3.get())

    def btn_transmitt_4_pressed_action(self):
        self.serialport_sendbytes_from_String(self.text_field4.get())

    def btn_transmitt_5_pressed_action(self):
        self.serialport_sendbytes_from_String(self.text_field5.get())

    def btn_transmitt_hex_pressed_action(self):
        if self.serialport.is_open and self.checkbox_hex_mode_value.get() == True:
            self.hex_text_decode(self.text_field_for_hex.get())

    def checkbox_timeline_mode_pressed_action(self):
        self.textarea1.config(state="normal")
        self.textarea1.insert(tk.END, "\n")
        self.textarea1.config(state="disabled")

    def checkbox_hex_mode_selected_action(self):
        self.hex_mode_object_control()

    def timer_callback(self):
        try:
            if self.serialport.is_open and self.serialport.in_waiting > 0:
                self.textarea1.config(state="normal")
                read_data = self.serialport.read_all()  # read_all return a bytes
                if self.checkbox_hex_mode_value.get() == True:  # Hex mode print out
                    if self.checkbox_timeline_mode_value.get() == True:
                        self.textarea1.insert(tk.END, f"{datetime.datetime.now()} > ")
                    self.textarea1.insert(
                        tk.END, self.convert2hexstring(read_data) + "\n"
                    )
                else:  # character mode print out
                    if self.checkbox_timeline_mode_value.get() == True:
                        self.textarea1.insert(
                            tk.END,
                            f"{datetime.datetime.now()} > {self.convert2string(read_data)}\n",
                        )
                    else:
                        self.textarea1.insert(tk.END, self.convert2string(read_data))
                self.textarea1.config(state="disabled")
        except OSError as e:
            print(f"In timer callback catch error {e}")
        if self.checkbox_scoll2bottom_value.get() == True:
            self.textarea1.config(state="normal")
            self.textarea1.see(tk.END)
            self.textarea1.config(state="disabled")

    def timer_start(self):
        threading.Thread(target=self.timer_thread).start()

    def timer_stop(self):
        self.timer_stop_event.set()

    def timer_thread(self):
        while not self.timer_stop_event.is_set():
            self.timer_callback()
            self.timer_stop_event.wait(self.timer_interval)

    def convert2hexstring(self, input):
        if not isinstance(input, bytes):
            return None
        byte_arrary = [int(byte) for byte in input]
        return_string = ""
        for byte in byte_arrary:
            return_string += f"0x{byte:02X},"
        return_string = return_string.rstrip(",")
        return return_string

    def convert2string(self, input):
        if not isinstance(input, bytes):
            return None
        byte_arrary = [int(byte) for byte in input]
        return_string = ""
        for byte in byte_arrary:
            if byte >= 32 and byte <= 126:
                return_string += f"{chr(byte)}"
            elif byte == 10:  # 0x0A
                return_string += "\n"
            elif byte == 13:  # 0x0D
                if self.checkbox_treat_cr_as_lf_value.get() == True:
                    return_string += "\n"
                else:
                    return_string += "\r"
            else:
                return_string += f"[0x{byte:02X}]"
        return return_string

    def Ascii2Hex(self, ascii_hex):
        return_hex = -1
        if ascii_hex >= 48 and ascii_hex <= 57:
            return_hex = ascii_hex
            return_hex -= 48
        elif ascii_hex >= 65 and ascii_hex <= 70:
            return_hex = ascii_hex
            return_hex -= 55
        elif ascii_hex >= 97 and ascii_hex <= 102:
            return_hex = ascii_hex
            return_hex -= 87
        return return_hex

    def hex_text_decode(self, hex_format_string):
        if not isinstance(hex_format_string, str):
            return None
        string2bytesArray = bytes(hex_format_string, "UTF-8")  # return bytes array
        bytes_array = []
        header = 0
        get_byte = 0
        for b in string2bytesArray:
            if header == 0:
                if b == 48:
                    header = 1
                else:
                    header = -1
            elif header == 1:
                if b == 120:
                    header = 2
                else:
                    header = -1
            elif header == 2:
                get_byte = self.Ascii2Hex(b)
                if get_byte == -1:
                    header = -1
                else:
                    header = 3
            elif header == 3:
                header = self.Ascii2Hex(b)
                if not (header == -1):
                    get_byte <<= 4
                    get_byte += header
                    header = 4
            elif header == 4:
                header = 0
                if b == 32 or b == 44:
                    # print(f"0x{get_byte:02X}")
                    bytes_array.append(get_byte)
                    get_byte = 0
                else:
                    header = -1
            elif header == -1:
                print("Invalid input format. Input should be 0x__,0x__,...")
                return None
        if get_byte != 0:
            bytes_array.append(get_byte)
        # uncommnet below for debug purpose
        # i = 0
        # if not header == -1:
        #     for element in bytes_array:
        #         i += 1
        #         print(f"{i}:{element:02X}")
        self.serialport.write(bytes_array)


def main():
    root = tk.Tk()
    try:
        app = PyTerminal(root)
        app.scan_serialports()
        app.update_combobox_value()
        app.timer_start()

        def on_closing():
            app.serialport_close()
            app.timer_stop()
            root.destroy()
            time.sleep(1)  # wait a little while for thread to end up by stop event

        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
    except ValueError as e:
        print("Initialization Failed:", e)


if __name__ == "__main__":
    main()
