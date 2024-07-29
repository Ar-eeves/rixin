import os
import shutil
import time
import qrcode

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
    
    directories = ["QR-Codes"]

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


# QR code generator and banner
def print_QR():
    columns = shutil.get_terminal_size().columns
    QR = """
[¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯]
[    ██████╗ ██████╗      ██████╗ ███████╗███╗   ██╗   ]
[   ██╔═══██╗██╔══██╗    ██╔════╝ ██╔════╝████╗  ██║   ]
[   ██║   ██║██████╔╝    ██║  ███╗█████╗  ██╔██╗ ██║   ]
[   ██║▄▄ ██║██╔══██╗    ██║   ██║██╔══╝  ██║╚██╗██║   ]
[   ╚██████╔╝██║  ██║    ╚██████╔╝███████╗██║ ╚████║   ]
[    ╚══▀▀═╝ ╚═╝  ╚═╝     ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ]
[______________________________________________________]
"""
    
    QR_lines = QR.strip().split('\n')
    os.system('cls' if os.name == 'nt' else 'clear')

    for line in QR_lines:
        print(RED + line.center(columns) + RESET)
def QR_GEN():

    print_QR()
    print("\n")
    
    url = input("Enter the URL of the site: ")

    qr = qrcode.make(url)
    type(qr)

    print(RED + "Created QR-Code for:", url + RESET , "\n")
    
    filename = input("Save file with the name: QR-")
    qrName =  "/QR-"+filename+".png"
    directory = input("Save in directory (Leave blank for QR-Codes folder): ")


    if directory != "":
        if os.path.isdir(directory) == True:
            print(RED + "Saved to:", directory + RESET)
            qr.save(directory + qrName)
            print(RED + "Showing file:" + RESET)
            os.startfile(directory + qrName) # arch no have startfile , change or remove?!?
            time.sleep(3)
        else:
            print("The directory " + directory + " does not exist: \n")
            print(RED + "Returning... " + RESET)
            time.sleep(3)
    else:
        defaultDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "QR-Codes")
        qr.save(defaultDIR + qrName)
        print(RED + "QR-Code saved to " + defaultDIR + RESET)
        print(RED + "Showing file:" + RESET)
        os.startfile(defaultDIR + qrName)  # arch no have startfile , change or remove?!?
        time.sleep(3)

if __name__ == "__main__":
    FolderCheck()
    print("\n")
    print(GREEN + "Folder check completed, Launching :)" + RESET)
    time.sleep(0.5)
    QR_GEN()
