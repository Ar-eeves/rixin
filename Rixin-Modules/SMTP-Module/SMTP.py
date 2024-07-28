import smtplib
from email.mime.text import MIMEText
from getpass import getpass
import random
import string
import os
import shutil
import time
import threading


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

# check folders are in place
def FolderCheck():

    localDIR = os.path.dirname(os.path.abspath(__file__))
    
    directories = ["Templates", "Logins"]

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

    def send_email(smtp_server, port, user, password, recipient, subject, body, times, randomize, increment, threader):
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
                    print(f"{MAGENTA}Email sent to {recipient} with subject '{current_subject}' and body '{current_body}'({total_sends}){RESET}")
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


        if threader == "yes":
            print(MAGENTA_bg+"THREADING ENABLED: STARTING"+RESET+"\n")
            threads = [threading.Thread(target=send_single_email, args=(i,)) for i in range(times)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
        else:
            print(MAGENTA_bg+"THREADING DISABLED: STARTING"+RESET+"\n")
            for i in range(times):
                
                send_single_email(i)

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
            subject = input("\nEnter email subject: ")
            print("")
        
        return subject, body


    def main():
        smtp_server = "smtp.gmail.com"
        port = 587
        script_dir = os.path.dirname(os.path.abspath(__file__))

        recent_file = os.path.join(script_dir, "Logins", "Recent.txt")
        LastLogin = open(recent_file).read()

        if not os.path.exists(recent_file):
            with open(recent_file, "w") as f:
                pass  
            print(RED + f"Created missing file: {recent_file}" + RESET)



        # auto login
        saved = input("Use last saved details? (yes/no): ").strip().lower() == "yes"
        if saved:
            script_dir = os.path.dirname(os.path.abspath(__file__))
        
            if os.path.exists(recent_file):
                user, password = LastLogin.split(":")
                print(MAGENTA+"\nLogging in as: "+user+RESET)
            print("")
        
        else:   # manual login and saving details
            select = input("Select from saved list? (yes/no): ").strip().lower() == "yes"
            if select:
                print("")
                Logins_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Logins")
                Logins = [f for f in os.listdir(Logins_dir) if os.path.isfile(os.path.join(Logins_dir, f))]

                if not Logins:
                    print("No Logins found in the 'Logins' folder.")
                    time.sleep(3)
                    return None, None

                print("Available Logins:")
                for idx, Login in enumerate(Logins):
                    print(f"{idx + 1}: {Login}")

                choice = int(input("Choose a template number or enter 0 to quit: ")) - 1

                if choice == -1: #if 0 is selected exit
                    print(RED+"No logins selected"+RESET+"\nExiting...")
                    time.sleep(3)
                    exit()
                else:
                    print(Logins[choice])
                    with open(os.path.join(Logins_dir, Logins[choice]), "r") as f:
                        credentials = f.read()
                        user, password = credentials.split(":")
                        print(MAGENTA+"\nLogging in as: "+user+RESET)
                        with open(os.path.join(script_dir, "Logins", "Recent.txt"), "w") as f:
                            f.write(user+":"+password)
                    print("")
                

            else:
                user = input("Enter your Gmail address: ")
                password = getpass("Enter your app password: ")
                with open(os.path.join(script_dir, "Logins", "recent.txt"), "w") as f:
                    f.write(user+":"+password)
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

        threader = input(MAGENTA_bg+"Enable threading, this may lead to rate limiting. (yes/no):"+RESET+" ").strip().lower()

        send_email(smtp_server, port, user, password, recipient, subject, body, times, randomize, increment, threader)

    if __name__ == "__main__":
        main()

if __name__ == "__main__":
    FolderCheck()
    print("\n")
    print(GREEN + "Folder check completed, Launching :)" + RESET)
    time.sleep(0.5)
    GMAIL_SMTP()