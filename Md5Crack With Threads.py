### MD 5 Cracker With Manual Threading ##

import hashlib
import time
import colorama
from termcolor import colored
from termcolor import colored, cprint


colorama.init() # initializing colorama.

def get_wordlist(wordlist_path):     #Function to get the location of the wordlist.
    import os
    
    if os.path.isfile(wordlist_path) == True:
        return 1
    
    else:
        print("Please enter the path of wordlist correctly!")
        user_args()
    
def crack_md5(wordlist_path,hash_to_crack,Frange,Lrange,verbose_mode,start_time):   # Pass 3 args hash_to_crack, Frange, Lrange
    wordlist = open(wordlist_path,'r',encoding='ISO-8859-1')
    words = wordlist.readlines() #Open the wordlist!
    #print(len(length.readlines())
    for x in range(Frange,Lrange):
        req = words[x]
        req = req.strip()  # To remove new line
        try_hash = hashlib.md5(str(req).encode("utf-8")).hexdigest()

        if (hash_to_crack == try_hash):
            cprint(">> ",'blue','on_grey',attrs=["bold"],end='')
            print("Cracked the hashed!")
            cprint(">> ",'blue','on_grey',attrs=["bold"],end='')
            print("Hash: {}, DeHashed: {}".format(hash_to_crack,req))
            Cracked(start_time)
        elif(verbose_mode == "1"):
            print("Hash_To_Cracked: {} | Trying hash: {} | Dehash: {}".format(hash_to_crack,try_hash,req))
            
def set_threads(wordlist_path,hash_to_crack,threads,verbose):
    import threading
    
    print("\n")
    start_index = []

    wordlist_read = open(wordlist_path,'r',encoding='ISO-8859-1') # Read the wordlist.
    wordlist = wordlist_read.readlines()

    # Now, did the right calculation.
    for x in range(0,len(wordlist),len(wordlist) // threads):
        start_index.append(x)

    # If we don't get the final value.
    if start_index[-1] != len(wordlist):
        start_index.append(len(wordlist))

    # Try to make it even.
    if len(start_index) % 2 != 0:
        start_index.pop()
        start_index.pop()
        start_index.append(len(wordlist))
    # The upper calculation is perfect!

    print(start_index)        

    args1 = 0
    args2 = 1
    start_time = time.time() #current time!
    print("\n\n")
    cprint("  ==============================================================================================","red","on_grey",attrs=["bold"])
    cprint("  ||  [+] Wordlist = {}                             ".format(str(wordlist_path)),"red","on_grey",attrs=["bold"])
    cprint("  ||  [+] Hash to crack = {}".format(hash_to_crack),"red","on_grey",attrs=["bold"])
    cprint("  ||  [+] Threads = {}".format(threads),"red","on_grey",attrs=["bold"])
    cprint("  ||  [+] Hash type = MD5                           ","red","on_grey",attrs=["bold"])
    cprint("  ==============================================================================================","red","on_grey",attrs=["bold"])
    cprint("Status: Cracking..........","red","on_grey",attrs=["bold"])

    threads_list = []
    
    while (args2 != len(start_index)):
        threads = threading.Thread(target=crack_md5, args=(wordlist_path,hash_to_crack,start_index[args1],start_index[args2],verbose,start_time))
        threads_list.append(threads)
        args1 += 1
        args2 += 1

    for y in threads_list:
        y.start()

    for z in threads_list:
        z.join()

def Cracked(start_time):
    import time
    import os
    
    cprint(">> ",'blue','on_grey',attrs=["bold"],end='')
    cprint("Cracked in -------- %.2fs Seconds ----------\n\n" % (time.time() - start_time),'red','on_grey',attrs=["bold"])
    os.system("exit")
    
def design():
    cprint("""                                                                                                                                                             
      __  ___ ____   ______   ______                    __              
     /  |/  // __ \ / ____/  / ____/_____ ____ _ _____ / /__ ___   _____
    / /|_/ // / / //___ \   / /    / ___// __ `// ___// //_// _ \ / ___/
   / /  / // /_/ /____/ /  / /___ / /   / /_/ // /__ / ,<  /  __// /    
  /_/  /_//_____//_____/   \____//_/    \__,_/ \___//_/|_| \___//_/              
                                                                     - with Love by Varun     
                                                                                                                                   
  Note: Very sorry to inform you all that this tool currently only supports ISO-8859-1 encoded wordlists

  Options: -h -> for help  |   man -> for manual   | help -> for help

  Usages: -w rockyou.txt -hash 5f46ff8adbbde309ba0edfd503897ce8 -t 3
""",'green','on_grey',attrs=["bold"])


def user_args():
    import os
    import subprocess
    
    cprint(" {} >> ".format(os.getcwd()),'blue','on_grey',attrs=["bold"],end='')
    user_input = input().lower()

    if (user_input == "-h" or user_input == "help"):
        help()

    elif (user_input == "man"):
        man()

#    elif (user_input == "dir" or user_input == "ls"):
#        output = subprocess.getoutput("dir")
#        print(output)
#        user_args()

    elif (len(user_input) > 41):
        # To get the wordlist
        wordlist_path = ""
        threads = ""
        hash_to_crack = ""
        verbose = 0
        search = user_input.find("-w")
        
        try:
            while(user_input[search+3] != " "):
                wordlist_path += user_input[search+3]
                search += 1
        except IndexError:
            pass

        # To get the threads value
        search = user_input.find("-t")
        try:
            while (user_input[search+3] != " "):
                threads += user_input[search+3]
                search += 1
        except IndexError:
            pass

        # To get the hash
        search = user_input.find("-hash")
        try:
            while(user_input[search+6] != " "):
                hash_to_crack += user_input[search+6]
                search += 1

        except IndexError:
            pass        

        if (search == user_input.find("-v")):
             verbose = 1
             
        # Test if the wordlist is legit or not!
        test_wordlist = get_wordlist(wordlist_path)

        # Test if md5 hash is correct or not?
        if len(hash_to_crack) != 32:
            print("MD5 hash is not correct!, we only support plain md5hash")
            user_args()

        # If all these tests succeed, then we will start our hash cracker function.
        set_threads(wordlist_path,hash_to_crack,int(threads),verbose)
        
    elif(user_input == "pwd"):
        print(os.getcwd())
        user_args()

    elif(user_input == "dir" or user_input == "ls -la" or user_input == "ls"):
        for x in os.listdir():
            print(" ", x)
        user_args()

    elif(user_input == "cls" or user_input == "clear"):
        subprocess.run("cls",shell=True)

    elif (user_input == "design"):
        design()
        user_args()

    elif(user_input[:2] == "cd" and user_input[2] == " "):
        # To change directory
        other_string = "" # Rest of the string used for chaning the directory!
        search = user_input.find("cd")
        if (len(user_input) > 1):
            other_string = user_input[3:]
            # If user uses ..
            if (other_string == ".."):
                current_dir = os.getcwd()
                current_dir_dashesh = current_dir.find("\\")
                current_dir_dashesh = current_dir[::-1]
                counter = 0
                to_remove = "" # Directory to remove
                try:
                    while(current_dir_dashesh[counter] != "\\"):
                        to_remove += current_dir_dashesh[counter]
                        counter += 1
                except IndexError:
                    pass

                to_remove = to_remove[::-1] # This is the directory path which is to be removed!
                current_dir = current_dir.replace(to_remove,"")
                os.chdir(current_dir.capitalize())
                
            # If user want's to change the directory via a defined path
            elif (len(other_string) > 1):
                try:
                    os.chdir(other_string.capitalize())
                    
                except Exception:
                    print("This is not a directory!")

            else:
                print("Invalid command used with cd")

    else:
        print("This command does not exists, Please use -h for help or man for manual")
        
    user_args()
#set_threads()

def help():
    print("""\nFlags in the program:
    -w    -> For defining the location of the wordlist
    -t    -> For defining the numbers of threads to use
    -hash -> For defining the hash to crack
    -v    -> For verbose mode

    example: To crack a hash with 3 threads.
    -w rockyou.txt -hash 5f46ff8adbbde309ba0edfd503897ce8 -t 3
    """)
    user_args()

def man():
    cprint(" Welcome to the program, This program is made for cracking md5 hashesh, Specifically for windows",'green','on_grey')
    user_args()

design()
user_args()

input("Press Enter Key To Exit")

#set_threads()  #Threads function.
