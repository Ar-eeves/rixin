import smtplib
from email.mime.text import MIMEText
from getpass import getpass
import random
import string
import os
import shutil
import time
import qrcode
import threading
import subprocess
import platform
from discord_webhook import DiscordWebhook

#todo
#encrypt username and password for smtp
#clean code
#more modules (aacu?!?!)

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
    
    directories = ["Templates", "QR-Codes", "Credentials"]

    print(RED_bg + "Created and tested on windows, expect bugs on other OS *cough cough arch*" + RESET)
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
[¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯]
[           ██████╗ ██╗██╗  ██╗██╗███╗   ██╗           ]
[           ██╔══██╗██║╚██╗██╔╝██║████╗  ██║           ]
[           ██████╔╝██║ ╚███╔╝ ██║██╔██╗ ██║           ]
[           ██╔══██╗██║ ██╔██╗ ██║██║╚██╗██║           ]
[           ██║  ██║██║██╔╝ ██╗██║██║ ╚████║           ]
[           ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝           ]
[                                                      ]
[ Rapid Intrusion eXploitation -- Intelligence Network ]
[______________________________________________________]
"""
    
    namecard_lines = namecard.strip().split('\n')
    os.system('cls' if os.name == 'nt' else 'clear')

    for line in namecard_lines:
        print(GREEN + line.center(columns) + RESET)

# Gmail smtp threader     banner and sender
def print_SMTP():
    columns = shutil.get_terminal_size().columns
    SMTP = """
[¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯]
[          ███████╗███╗   ███╗████████╗██████╗         ]
[          ██╔════╝████╗ ████║╚══██╔══╝██╔══██╗        ]
[          ███████╗██╔████╔██║   ██║   ██████╔╝        ]
[           ════██║██║╚██╔╝██║   ██║   ██╔═══╝         ]
[          ███████║██║ ╚═╝ ██║   ██║   ██║             ]
[           ══════╝╚═╝     ╚═╝   ╚═╝   ╚═╝             ]
[                                                      ]
[ Rapid Intrusion eXploitation -- Intelligence Network ]
[______________________________________________________]
"""
    
    SMTP_lines = SMTP.strip().split('\n')
    os.system('cls' if os.name == 'nt' else 'clear')

    for line in SMTP_lines:
        print(MAGENTA + line.center(columns) + RESET)
def GMAIL_SMTP():

    print_SMTP()
    print("\n")

    def generate_random_string(length):
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))


    ## threader

    def send_email(smtp_server, port, user, password, recipient, subject, body, times, randomize, increment):
        total_errors = 0
        total_sends = 0
        lock = threading.Lock()

        def send_single_email(index):
            nonlocal total_errors, total_sends
            max_retries = 5
            initial_delay = 1

            for attempt in range(max_retries):
                try:
                    current_subject = (
                        generate_random_string(10) if randomize 
                        else f"{subject} : {index}" if increment == "yes" 
                        else subject
                    )
                    current_body = generate_random_string(50) if randomize else body
                    msg = MIMEText(current_body)
                    msg['Subject'] = current_subject
                    msg['From'] = user
                    msg['To'] = recipient

                    with smtplib.SMTP(smtp_server, port) as server:
                        server.starttls()
                        server.login(user, password)
                        server.sendmail(user, recipient, msg.as_string())
                    
                    with lock:
                        total_sends += 1
                    print(f"{MAGENTA}Email sent to {recipient} with subject '{current_subject}' and body'{current_body}'{RESET}")
                    break
                except smtplib.SMTPServerDisconnected:
                    print(RED + "Connection unexpectedly closed. Retrying..." + RESET)
                except smtplib.SMTPException as e:
                    if 400 <= e.smtp_code < 500:
                        print(RED + f"Temporary error: {e}. Retrying..." + RESET)
                    else:
                        print(f"{RED}An error occurred: {e}{RESET}")
                        break
                except Exception as e:
                    print(f"{RED}An unexpected error occurred: {e}{RESET}")
                    break
                finally:
                    if 'total_errors' in locals():
                        total_errors += 1
                    time.sleep(initial_delay * (2 ** attempt))

        threads = [threading.Thread(target=send_single_email, args=(i,)) for i in range(times)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        total_errors = total_errors - total_sends
        fail_rate = (total_errors / (total_sends + total_errors)) * 100 if (total_sends + total_errors) > 0 else 0
        print(f"{GREEN}Total Emails Sent: {total_sends}{RESET}")
        print(f"{RED}Total Errors: {total_errors}{RESET}")
        print(f"{YELLOW}Fail Rate: {fail_rate:.2f}%{RESET}")

        time.sleep(5)

    ## end of threader

    def choose_template():
        templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Templates")
        templates = [f for f in os.listdir(templates_dir) if os.path.isfile(os.path.join(templates_dir, f))]

        if not templates:
            print("No templates found in the 'Templates' folder.")
            time.sleep(3)
            return None, None

        print("Available templates:")
        for idx, template in enumerate(templates):
            print(f"{idx + 1}: {template}")

        choice = int(input("Choose a template number or enter 0 to write your own: ")) - 1

        if choice == -1:
            subject = input("Enter email subject: ")
            body = input("Enter email body: ")
            print("")
        else:
            with open(os.path.join(templates_dir, templates[choice]), "r") as f:
                body = f.read()
            subject = input("Enter email subject: ")
            print("")
        
        return subject, body


    def main():
        smtp_server = "smtp.gmail.com"
        port = 587
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # checks to make sure credential files exist
        user_file = os.path.join(script_dir, "Credentials", "SavedUser.txt")
        password_file = os.path.join(script_dir, "Credentials", "SavedApp.txt")

        # Ensure the files exist, create them if not
        if not os.path.exists(user_file):
            with open(user_file, "w") as f:
                pass  # Create an empty file
            print(RED + f"Created missing file: {user_file}" + RESET)

        if not os.path.exists(password_file):
            with open(password_file, "w") as f:
                pass  # Create an empty file
            print(RED + f"Created missing file: {password_file}" + RESET)


        # auto login
        saved = input("Use last saved details? (yes/no): ").strip().lower() == "yes"
        if saved:
            script_dir = os.path.dirname(os.path.abspath(__file__))
        
            if os.path.exists(user_file) and os.path.exists(password_file):
                with open(user_file, "r") as f:
                    user = f.read().strip()
                with open(password_file, "r") as f:
                    password = f.read().strip()
                print(f"Using {user}: \n")
            else:
                print("Saved user or password file does not exist.")
                time.sleep(3)
                return

        else:   # manual login and saving details
            user = input("Enter your Gmail address: ")
            password = getpass("Enter your app password: ")
            with open(os.path.join(script_dir, "Credentials", "SavedUser.txt"), "w") as f:
                f.write(user)
            with open(os.path.join(script_dir, "Credentials", "SavedApp.txt"), "w") as f:
                f.write(password)
            print("Saved new details:")

        recipient = input("Enter recipient email: ")
        use_template = input("Do you want to use an email template? (yes/no): ").strip().lower() == 'yes'
        print("")

        if use_template:
            subject, body = choose_template()
        else:
            subject = input("Enter email subject: ")
            body = input("Enter email body: ")
            print()

        if not subject or not body:
            print("No subject or body specified. Exiting.")
            time.sleep(3)
            return

        randomize = input("Randomize subject and body for each email? (yes/no): ").strip().lower() == 'yes'
        increment = input("Increment each subject? (yes/no): ").strip().lower()
        print("")
        times = int(input("Enter number of times to send the email: "))

        send_email(smtp_server, port, user, password, recipient, subject, body, times, randomize, increment)

    if __name__ == "__main__":
        main()


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
[                                                      ]
[ Rapid Intrusion eXploitation -- Intelligence Network ]
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

def print_HOOK():
    columns = shutil.get_terminal_size().columns
    HOOK = """
[¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯]
[          ██╗  ██╗ ██████╗  ██████╗ ██╗  ██╗          ]
[          ██║  ██║██╔═══██╗██╔═══██╗██║ ██╔╝          ]
[          ███████║██║   ██║██║   ██║█████╔╝           ]
[          ██╔══██║██║   ██║██║   ██║██╔═██╗           ]
[          ██║  ██║╚██████╔╝╚██████╔╝██║  ██╗          ]
[          ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝          ]
[                                                      ]
[ Rapid Intrusion eXploitation -- Intelligence Network ]
[______________________________________________________]
"""
    
    HOOK_lines = HOOK.strip().split('\n')
    os.system('cls' if os.name == 'nt' else 'clear')

    for line in HOOK_lines:
        print(BLUE + line.center(columns) + RESET)

def Webhooker():
    print_HOOK()
    print("\n")

    print(BLUE_bg+"WARNING: You may be rate limited by discord and have your IP temporarily blocked.\nIf you recieve many rate limits, wait and try again later."+RESET)
    print()

    def generate_random_string(length):
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    url = input("Enter the webhook URL: ")
    content = input("Enter the message to send: ")
    print("")

    randomize = input("Randomize the text sent? (yes/no): ").strip().lower() == "yes"
    times = int(input("Enter number of times to send the text: "))
    print("")

    threader = input(BLUE_bg+"Enable threading, WARNING this may lead to rate limiting. (yes/no):"+RESET+" ").strip().lower()
    print("")
    
    def SendHook(url, content, randomize, times, threader):
        
        lock = threading.Lock()
                            
        def Send():
            nonlocal content

            if randomize:
                content = generate_random_string(50)

            webhook = DiscordWebhook(url=url, rate_limit_retry=True, content=content)
            response = webhook.execute()

            if response.status_code == 200:
                print(BLUE+"Sent message to '"+ url+"' with content'"+content+"'"+RESET)
                return response
            elif response.status_code == 429:
                retry_counter += 1
                retry_after = int(response.headers.get("Retry-After", 1)) 
                print(RED+"Rate limited. Retrying after {retry_after} seconds..."+RESET)
                time.sleep(retry_after)
            else:
                print(RED+"Failed to send webhook. Status code: {response.status_code}"+RESET)
                return response
            print(RED+"Exceeded maximum retries."+RESET)
            return None

        if threader == "yes":
            print(BLUE_bg+"THREADING ENABLED: STARTING"+RESET)
            threads = [threading.Thread(target=Send) for i in range(times)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
                
        else:
            print(BLUE_bg+"THREADING DISABLED: STARTING"+RESET)
            for i in range(times):
                Send()
                time.sleep(0.1)

        print(BLUE_bg+"\n Webhook sending complete \nClosing..."+RESET)
        time.sleep(3)

    SendHook(url, content, randomize, times, threader)

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
            GMAIL_SMTP()
        elif choice == '2':
            QR_GEN()
        elif choice == '3':
            Webhooker()
        elif choice == '4':
            print_menu()
        elif choice == '99':
            exit()
            
        else:
            print_namecard()
            print("Invalid choice. Please enter a module that is listed.")

if __name__ == "__main__":
    FolderCheck()
    print("\n")
    print(GREEN + "Folder check completed, Launching :)" + RESET)
    time.sleep(0.5)
    main()