import threading
import _thread
import tkinter as tk
import sys

""" Shows a popup with the alarm time & a button to cancel the alarm """

class Popup(threading.Thread):

    def __init__(self, alarmtime):
        threading.Thread.__init__(self)
        self.__alarmtime = alarmtime
        self.daemon = True
        self.start()

    def run(self):
        self.root = tk.Tk()
        self.root.title("RasPi Alarm")

        # Message box info with alarm time
        message = "Alarm is set at {}".format(self.__alarmtime)
        msg = tk.Label(self.root, padx = 30, pady = 50, text = message)
        msg.pack()

        # Cancel button
        cancel = tk.Button(self.root, padx = 100, pady = 10, text = "Cancel Alarm", command = self.root.quit)
        cancel.pack()

        # start GUI
        self.root.mainloop()
        # when cancel button is clicked, mainloop exits and code continues:

        # create flag file to cancel alarm
        with open('cancel_alarm', 'w'):
            print("Created flag file 'cancel_alarm'")
        # destroy popup window
        self.root.quit()
        print("Alarm cancelled. Give loop some time until sleep is done")
