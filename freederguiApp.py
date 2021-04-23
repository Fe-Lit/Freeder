from kivy.app import App
from kivy.core import text

from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.widget import Widget
# The Builder is responsible for creating a Parser for parsing a kv file
from kivy.lang import Builder
# The Properties classes are used when you create an EventDispatcher.
#from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from freedprotocolparser import freedprotocolparser
from kaitaistruct import KaitaiStream, BytesIO

import socket

UDP_IP = "192.168.2.255"
UDP_PORT = 7002
BUFFERSIZE = 128  # buffer size is 128 bytes


class freedatavalues:

    def __init__(self, device_IP="127.0.0.1", device_port=7001):
        self.ip = device_IP
        self.port = device_port
        self.buffersize = 256
        # Zur berechnung der Skalierte werte
        # unscaled = 24bit unsigned int
        self.focus = 0
        self.min_focus = 100000
        self.max_focus = 0
        self.zoom = 0
        self.min_zoom = 100000
        self.max_zoom = 0
        print("+++ Neues Objekt erstellt +++")

    def start(self):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.my_socket.bind((self.ip, self.port))
        print("+++ Socket erstellt +++")

    def stop(self):
        self.my_socket.close()
        print("--- Socket geschlossen ---")

    def refresh_data(self):
        try:
            self.packet_data, self.address = self.my_socket.recvfrom(
                self.buffersize)
        except:
            print("!!!!! Fehler beim Lesen aus dem Socket !!!!!")

    def get_x_m(self):
        return ((freedprotocolparser(KaitaiStream(BytesIO(self.packet_data))).x_pos.value) / 64000)

    def get_y_m(self):
        return ((freedprotocolparser(KaitaiStream(BytesIO(self.packet_data))).y_pos.value) / 64000)

    def get_z_m(self):
        # height, upwards -> +
        return ((freedprotocolparser(KaitaiStream(BytesIO(self.packet_data))).z_pos.value) / 64000)

    def get_pan(self):
        return ((freedprotocolparser(KaitaiStream(BytesIO(self.packet_data))).pan_angle.value / 32768))

    def get_tilt(self):
        return ((freedprotocolparser(KaitaiStream(BytesIO(self.packet_data))).tilt_angle.value / 32768))

    def get_roll(self):
        return ((freedprotocolparser(KaitaiStream(BytesIO(self.packet_data))).roll_angle.value / 32768))

    def get_raw_zoom(self):
        self.zoom = freedprotocolparser(KaitaiStream(
            BytesIO(self.packet_data))).zoom.value
        if (self.zoom < self.min_zoom):
            self.min_zoom = self.zoom
        if (self.zoom > self.max_zoom):
            self.max_zoom = self.zoom
        return self.zoom

    def get_raw_focus(self):
        self.focus = freedprotocolparser(KaitaiStream(
            BytesIO(self.packet_data))).focus.value
        if (self.focus < self.min_focus):
            self.min_focus = self.focus
        if (self.focus > self.max_focus):
            self.max_focus = self.focus
        return self.focus

    def get_zoom_percent(self):
        try:
            return round(((self.get_raw_zoom()-self.min_zoom)/(self.max_zoom-self.min_zoom))*100, 0)
        except:
            return "NaN"

    def get_focus_percent(self):
        try:
            return round(((self.get_raw_focus()-self.min_focus)/(self.max_focus-self.min_focus))*100, 0)
        except:
            return "NaN"


def scale_number(unscaled, from_min, from_max, to_min=0, to_max=100):
    # Scale a Value
    # default between 0/100 = Percent
    return (to_max-to_min)*(unscaled-from_min)/(from_max-from_min)+to_min


class my_gui(Widget):
    ip_prop = ObjectProperty(None)
    port_prop = ObjectProperty(None)
    out_label = ObjectProperty(None)
    start_btn = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(my_gui, self).__init__(**kwargs)
        self.is_running = 0
        self.freed_initialized = 0

        Clock.schedule_interval(self.programm_logic, .1)

    def btn(self):
        #print("Name:", self.ip.text, "email:", self.port.text)
        #self.ip.text = ""
        #self.port.text = ""
        self.ip = self.ip_prop.text
        self.port = self.port_prop.text
        print("Target_IP:", self.ip, "Target_Port:", self.port)

        # Ausgabe starten
        if self.is_running == 0:
            print("GO")
            self.start_btn.text = "STOP"
            self.is_running = 1
            Clock.unschedule(self.programm_logic)
            Clock.schedule_interval(self.programm_logic, 0.1)
            print("Ausgabe gestartet")

        # Ausgabe Stoppen
        elif self.is_running == 1:
            Clock.unschedule(self.programm_logic)
            print("STOP")
            self.start_btn.text = "START"
            self.out_label.text = "PAUSIERT"
            self.is_running = 0

    def programm_logic(self, dt):
        if self.is_running == 1:
            if self.freed_initialized == 0:
                self.kran = freedatavalues(self.ip, int(self.port))
                self.kran.start()
                self.freed_initialized = 1
            self.kran.refresh_data()
            #self.out_label.text = str(self.kran.get_x_m())+str(self.kran.get_pan())
            self.out_label.text=self.print_formated_values()
        elif self.is_running == 0:
            if self.freed_initialized == 1:
                self.kran.stop()
                self.freed_initialized = 0

    def print_formated_values(self):
        try:
            """
            self.datenstring = "X:" + self.kran.get_x_m() + "m Y:"+self.kran.get_y_m() + "m Z:" + self.kran.get_z_m() + "m Pan:" + self.kran.get_pan()+"° Tilt:" + self.kran.get_tilt() + "° Roll:" + \
                self.kran.get_roll() + "° Zoom:" + self.kran.get_raw_zoom() + "(" + self.kran.get_zoom_percent() + \
                "%) Focus:" + \
                self.kran.get_raw_focus() + "(" + self.kran.get_focus_percent() + "%)"
            """
            self.datenstring="Values from: "+str(self.ip)+" Port: "+str(self.port)+"\n"
            self.datenstring=self.datenstring+(len(self.datenstring)*"- ")+"\n"
            self.datenstring=self.datenstring+"X: "+(f"{self.kran.get_x_m():5.3f}")
            self.datenstring=self.datenstring+"m Y: "+(f"{self.kran.get_y_m():5.3f}")
            self.datenstring=self.datenstring+"m Z: "+(f"{self.kran.get_z_m():5.3f}")
            self.datenstring=self.datenstring+"m\n"
            self.datenstring=self.datenstring+"P: "+(f"{self.kran.get_pan():5.3f}")
            self.datenstring=self.datenstring+"°  T: "+(f"{self.kran.get_tilt():5.3f}")
            self.datenstring=self.datenstring+"°  R: "+(f"{self.kran.get_roll():5.3f}")
            self.datenstring=self.datenstring+"°\n"
            self.datenstring=self.datenstring+"Zoom: "+str(self.kran.get_raw_zoom())+"(" + str(self.kran.get_zoom_percent())+"%) Focus: "+str(self.kran.get_raw_focus()) + "(" + str(self.kran.get_focus_percent()) + "%)"

        except:
            self.datenstring = "Noch keine Daten ehalten"
        #print(self.datenstring)
        return self.datenstring


class freederguiApp(App):
    # Hauptprogramm??
    def build(self):
        return my_gui()


if __name__ == "__main__":
    app = freederguiApp()
    print("----------- Gui objekt erzeugt")
    app.run()
