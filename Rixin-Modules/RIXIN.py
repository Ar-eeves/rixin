import os
import shutil
import time
import subprocess
import platform

# colors for banners and etc
RED = '\x1b[31m'
GREEN = '\033[32m'
YELLOW = '\x1b[33m'
BLUE = '\x1b[34m'
MAGENTA = '\x1b[35m'
CYAN = '\x1b[36m'
WHITE = '\x1b[37m'
#BG colors
RED_bg = '\x1b[41m'
GREEN_bg = '\033[42m'
YELLOW_bg = '\x1b[43m'
BLUE_bg = '\x1b[44m'
MAGENTA_bg = '\x1b[45m'
CYAN_bg = '\x1b[46m'
WHITE_bg = '\x1b[47m'

RESET = '\033[0m'


# Checks required folders are in place
def FolderCheck():

    localDIR = os.path.dirname(os.path.abspath(__file__))
    
    directories = [ "SMTP-Module", "QRGEN-Module", "WEBHOOK-Module"]

    print(GREEN_bg + "Created and tested on windows, expect bugs on other OS *cough cough arch*" + RESET)
    print(GREEN +"Running folder check for:", str(directories) + RESET)
    print("\n")
    
    for directory in directories:
        dir_path = os.path.join(localDIR, directory)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
            print(RED_bg + f"Created missing directory: {dir_path}")
        else:
            print(GREEN + f"Directory already exists: {dir_path}")
 
# main banner
def print_namecard():
    columns = shutil.get_terminal_size().columns
    namecard = """
[‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾]
[           ██████╗ ██╗██╗  ██╗██╗███╗   ██╗           ]
[           ██╔══██╗██║╚██╗██╔╝██║████╗  ██║           ]
[           ██████╔╝██║ ╚███╔╝ ██║██╔██╗ ██║           ]
[           ██╔══██╗██║ ██╔██╗ ██║██║╚██╗██║           ]
[           ██║  ██║██║██╔╝ ██╗██║██║ ╚████║           ]
[           ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝           ]
[______________________________________________________]
"""
    
    namecard_lines = namecard.strip().split('\n')
    os.system('cls' if os.name == 'nt' else 'clear')

    for line in namecard_lines:
        print(GREEN + line.center(columns) + RESET)

def open_new_terminal(script_name):
    system = platform.system()
    script_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), script_name)

    print("opening")
    
    if system == "Windows":
        subprocess.Popen(["start", "cmd", "/c", f"python {script_path}"], shell=True)   
    elif system == "Linux":
        subprocess.Popen(["xterm", "--", "bash", "-c", f"python {script_path}"])
    else:
        raise Exception(f"Unsupported OS: {system}")
    
# main menu and menu chooser
def print_menu():
    # Menu options
    os.system('cls' if os.name == 'nt' else 'clear')
    print_namecard()
    menu = [
        MAGENTA+"1. Gmail SMTP"+RESET,
        RED+"2. QR-code generator"+RESET,
        BLUE+"3. Discord webhook sender"+RESET,
        GREEN+"4. Refresh"+RESET,
        "---------",
        YELLOW+"99. Exit"+RESET
    ]

    # Print the menu
    print("\nMenu:")
    for option in menu:
        print(option)

def main():
    while True:
        print_menu()
        choice = input("\nEnter your choice (1-99): ")

        if choice == '1':
            script_name = "SMTP-Module/SMTP.py"
            open_new_terminal(script_name)
        elif choice == '2':
            script_name = "QRGEN-Module/QRGEN.py"
            open_new_terminal(script_name)
        elif choice == '3':
            script_name = "WEBHOOK-Module/WEBHOOK.py"
            open_new_terminal(script_name)
        elif choice == '4':
            print_menu()
        elif choice == '99':
            print("Exiting...")
            break
        else:
            print_namecard()
            print("Invalid choice. Please enter a module that is listed.")

if __name__ == "__main__":
    FolderCheck()
    print("\n")
    print(GREEN + "Folder check completed, Launching :)" + RESET)
    time.sleep(0.5)
    main()
