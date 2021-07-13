from pynput import keyboard

def on_press(key):
    print("key {} pressed".format(key))



    if str(key) == 'key.esc':
        print("Exiting...")
        return False

with keyboard.Listener(
    on_press = on_press
    ) as listener:
    listener.join()
