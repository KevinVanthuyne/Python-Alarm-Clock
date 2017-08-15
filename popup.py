class Popup(threading.Thread):

""" Shows a popup with the alarm time & a button to cancel the alarm """

    def cancel(self):
        print("Alarm cancelled") # TODO alarm hiermee stoppen
        self.root.destroy()
        exitProgram()

    def __init__(self, alarmtime):
        threading.Thread.__init__(self)
        self.alarmtime = alarmtime
        self.daemon = True
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        self.root.title("RasPi Alarm")

        message = "Alarm is set at {}".format(self.alarmtime)
        msg = tk.Label(self.root, padx = 30, pady = 50, text = message)
        msg.pack()

        cancel = tk.Button(self.root, padx = 10, pady = 10, text = "Cancel Alarm", command = self.cancel)
        cancel.pack()

        self.root.mainloop()
