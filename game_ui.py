import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
import subprocess
import os
import time, threading
import paho.mqtt.client as mqtt
from tkwebview2.tkwebview2 import WebView2

class Application(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.stop_identifier = 1
        # self.a = 0 // globla variable a
        # self.b = 0 // globla variable b

        # self.bind_all('<KeyPress-w>', self.up_pressed)
        # self.bind_all('<KeyPress-a>', self.left_pressed)
        # self.bind_all('<KeyPress-d>', self.right_pressed)
        # self.bind_all('<KeyPress-s>', self.down_pressed)
        # self.bind_all('<KeyPress-q>', self.rotate_left_pressed)
        # self.bind_all('<KeyPress-e>', self.rotate_right_pressed)
        # self.bind_all('<KeyPress-t>', self.stop_pressed)
        # self.bind_all('<KeyPress-r>', self.restart_pressed)
        # self.bind_all('<KeyPress-c>', self.connect_pressed)
        # self.bind_all('<KeyRelease>', self.keyrelease)
        self.grid()
        self.create_widgets()

    def create_widgets(self):

        # Frame_0 Visual Feedback
        self.frame_0 = tk.LabelFrame(self, text = "Visual Feedback")
        ## Element -- Canvas
        # self.canvas = tk.Canvas(master = self.frame_0, width=400, height=300, background='white')
        self.webview = WebView2(self.frame_0, width=770, height=530)
        self.webview.load_url('https://superxh.github.io/ezuikit_video/index.html')
        ## Layout management
        # self.canvas.pack(side = tk.BOTTOM)
        self.webview.pack(side = tk.BOTTOM)

        # Tab_Switcher
        n =ttk.Notebook(self)
        ## Element -- Frame_1, 2, 3
        self.frame_1 = tk.LabelFrame(n, width=400)   # first page, which would get widgets gridded into it
        self.frame_2 = tk.LabelFrame(n, width=400)   # second page
        self.frame_3 = tk.LabelFrame(n, width=400)   # second page
        n.add(self.frame_1, text='Remote Driving')
        n.add(self.frame_2, text='Client Connect')
        n.add(self.frame_3, text='Logs Terminal')

        # Frame_1 -- Remote Driving
        # self.frame_1_1 = tk.LabelFrame(self.frame_1, height=200, width=200, text = "Controller")
        self.frame_1_2 = tk.LabelFrame(self.frame_1, height=200, width=400, text = "Status")
        # ## Frame_1_1 -- Controller
        # self.up_button = tk.Button(self.frame_1_1, text='^', command = self.button_pressed_up)
        # self.left_button = tk.Button(self.frame_1_1, text='<', command = self.button_pressed_left)
        # self.right_button = tk.Button(self.frame_1_1, text='>', command = self.button_pressed_right)
        # self.down_button = tk.Button(self.frame_1_1, text='*', command = self.button_pressed_down)

        # self.up_button.grid(row = 0, column = 1, sticky = tk.W)
        # self.left_button.grid(row = 1, column = 0, sticky = tk.W )
        # self.right_button.grid(row = 1, column = 2, sticky = tk.W )
        # self.down_button.grid(row = 1, column = 1, sticky = tk.W )

        ## Frame_1_2 -- Status
        self.throttle_label = tk.Label(self.frame_1_2, text='Throttle: ')
        # self.throttle_param = tk.Label(self.frame_1_2, text=str(10)+'Km/h')
        self.throttle_param = tk.Label(self.frame_1_2, text=str(0))
        self.brake_label = tk.Label(self.frame_1_2, text='brake: ')
        # self.brake_param = tk.Label(self.frame_1_2, text=str(0)+'%')
        self.brake_param = tk.Label(self.frame_1_2, text=str(0))
        self.direction_label = tk.Label(self.frame_1_2, text='Direction: ')
        # self.direction_param = tk.Label(self.frame_1_2, text=str(0)+'°')
        self.direction_param = tk.Label(self.frame_1_2, text=str(0))
        self.gear_label = tk.Label(self.frame_1_2, text='Gear: ')
        # self.gear_param = tk.Label(self.frame_1_2, text='I')
        self.gear_param = tk.Label(self.frame_1_2, text=str(0))

        self.throttle_label.grid(row = 0, column = 0, sticky = tk.W)
        self.throttle_param.grid(row = 0, column = 1, sticky = tk.W) 
        self.brake_label.grid(row = 0, column = 2, sticky = tk.W) 
        self.brake_param.grid(row = 0, column = 3, sticky = tk.W) 
        self.direction_label.grid(row = 1, column = 0, sticky = tk.W)
        self.direction_param.grid(row = 1, column = 1, sticky = tk.W)
        self.gear_label.grid(row = 1, column = 2, sticky = tk.W) 
        self.gear_param.grid(row = 1, column = 3, sticky = tk.W) 
        self.frame_1_2.columnconfigure(1, minsize = 75)
        self.frame_1_2.columnconfigure(3, minsize = 75)
        self.frame_1_2.rowconfigure(0, minsize = 25)
        self.frame_1_2.rowconfigure(1, minsize = 25)
        # self.frame_1_1.grid(row = 0, column = 0, sticky = tk.N)
        self.frame_1_2.grid(row = 0, column = 0, sticky = tk.W)

        # Frame_2 -- Client Connect
        self.server_label = tk.Label(self.frame_2, text='Server Address: ')
        self.server_entry = tk.Entry(self.frame_2)
        self.server_entry.insert(0, "broker-cn.emqx.io:1883")
        self.clientid_label = tk.Label(self.frame_2, text='Client ID: ')
        self.clientid_entry = tk.Entry(self.frame_2)
        self.clientid_entry.insert(0, "remote_receiver")
        self.connect_button = tk.Button(self.frame_2, text='Connect', command = self.connect_pressed)
        self.connect_label = tk.Label(self.frame_2, text='Status: ')
        self.connect_param = tk.Label(self.frame_2, text='Disconnected')

        self.server_label.grid(row = 0, column = 0, columnspan = 1, sticky = tk.W)
        self.server_entry.grid(row = 0, column = 1, columnspan = 2, sticky = tk.EW)
        self.clientid_label.grid(row = 1, column = 0, columnspan = 1, sticky = tk.W)
        self.clientid_entry.grid(row = 1, column = 1, columnspan = 1, sticky = tk.W)
        self.connect_button.grid(row = 1, column = 2, sticky = tk.E)
        self.connect_label.grid(row = 2, column = 0, columnspan = 1, sticky = tk.W)
        self.connect_param.grid(row = 2, column = 1, columnspan = 1, sticky = tk.W)

        # Frame_3 -- Logs Terminal
        self.terminal = scrolledtext.ScrolledText(self.frame_3, width = 50, height = 5, wrap = "none")
        self.terminal.grid(row = 0, column = 0, rowspan = 4, sticky = tk.E)

        # Overall Layout
        self.frame_0.grid(row = 0, column = 0)
        n.grid(row = 1, column = 0)

    # #################################
    # # Function KeyPress #############
    # #################################
    # def up_pressed(self, event):
    #     # print("^")
    #     self.up_button.configure(relief = 'sunken')
    #     self.up_button.invoke()
    # def left_pressed(self, event):
    #     # print("<")
    #     self.left_button.configure(relief = 'sunken')
    #     self.left_button.invoke()
    # def right_pressed(self, event):
    #     # print(">")
    #     self.right_button.configure(relief = 'sunken')
    #     self.right_button.invoke()
    # def down_pressed(self, event):
    #     # print("*")
    #     self.down_button.configure(relief = 'sunken')
    #     self.down_button.invoke()
    # def rotate_left_pressed(self, event):
    #         # print("*")
    #         self.mqtt_send(b'cmd_vel rotate_left\n')
    # def rotate_right_pressed(self, event):
    #         # print("*")
    #         self.mqtt_send(b'cmd_vel rotate_right\n')
    # def stop_pressed(self, event):
    #         self.mqtt_send(b'cmd_vel stop\n')
    # def restart_pressed(self, event):
    #         self.mqtt_send(b'cmd_vel restart\n')

    # def keyrelease(self, event):
    #     self.up_button.configure(relief = 'raised')
    #     self.left_button.configure(relief = 'raised')
    #     self.right_button.configure(relief = 'raised')
    #     self.down_button.configure(relief = 'raised')

    # def button_pressed_up(self):
    #         # print("^")
    #         self.mqtt_send(b'cmd_vel up\n')
    # def button_pressed_left(self):
    #         # print("<")
    #         self.mqtt_send(b'cmd_vel left\n')
    # def button_pressed_right(self):
    #         # print(">")
    #         self.mqtt_send(b'cmd_vel right\n')
    # def button_pressed_down(self):
    #         # print("*")
    #         self.mqtt_send(b'cmd_vel down\n')

    #################################
    # Function KeyPress #############
    #################################
    # def mqtt_thread(self):
    #     server = self.server_entry.get();
    #     clientid = self.clientid_entry.get();
    #     self.p = subprocess.Popen(["./send", server, clientid], cwd = "build", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    #     for line in iter(self.p.stdout.readline, b''):
    #         if not subprocess.Popen.poll(self.p) is None:
    #             if line == "":
    #                 break
    #         print (line.decode("utf-8"))
    #         if line.decode("utf-8") == "Connecting...OK\n":
    #             self.connect_param.config(text='Connected')
    #             self.connect_button.config(text='Disconnect', command = self.mqtt_disconnect)
    #         elif line.decode("utf-8") == "Disconnecting...OK\n":
    #             self.connect_param.config(text='Disconnected')
    #             self.connect_button.config(text='Connect', command = self.mqtt_connect)
    #         self.terminal.insert("end", line.decode("utf-8"))
    #     self.p.stdout.close()

    # def mqtt_connect(self):
    #     self.t = threading.Thread(target=self.mqtt_thread, name='mqttThread')
    #     self.t.start()

    # def mqtt_disconnect(self):
    #     self.mqtt_send(b'command \quit\n')

    # def mqtt_send(self, inputbytes):
    #     # inputbytes = b'laikago/fr hello\n'
    #     self.p.stdin.write(inputbytes)
    #     print (inputbytes.decode("utf-8"))
    #     self.p.stdin.flush()
    #     self.terminal.insert("end", inputbytes.decode("utf-8"))

    #################################
    # Function MQTT Receive##########
    #################################
    # The callback for when the client receives a CONNACK response from the server.
    def update_state(self, state_array):
        self.direction_param.configure(text = str(state_array[0]))
        self.throttle_param.configure(text = str(state_array[1]))
        self.brake_param.configure(text = str(state_array[2]))
        self.gear_param.configure(text = str(state_array[3]))

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("cmd_vel")
    
    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(msg.topic)
        mqtt_msg = msg.payload
        mqtt_msg = mqtt_msg.decode('utf8')
        mqtt_msg = mqtt_msg.split(",")
        for i in range(0, 4):
            mqtt_msg[i] =float(mqtt_msg[i])
        print(mqtt_msg)
        self.terminal.insert("end", str(mqtt_msg) + '\n')
        self.update_state(mqtt_msg)

    def receive_connect(self):
        server = self.server_entry.get().split(":");
        clientid = self.clientid_entry.get();

        self.client = mqtt.Client(clientid )
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(server[0], int(server[1]), 60)
        
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        self.client.loop_start()
        while(self.stop_identifier):{}
        self.client.loop_stop(force=True)

    def receive_disconnect(self):
        self.stop_identifier = 0
        self.connect_param.config(text='Disconnected')
        self.connect_button.config(text='Connect', command = self.connect_pressed)
        print("Disconnected")
        self.stop_identifier = 1

    def connect_pressed(self):
        self.connect_param.config(text='Connected')
        self.connect_button.config(text='Disconnect', command = self.receive_disconnect)
        self.t2 = threading.Thread(target=self.receive_connect, name='receiveThread')
        self.t2.start()

app = Application()
app.master.title('Remote Driver')
app.mainloop()
