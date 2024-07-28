import os
import shutil
import time
from discord_webhook import DiscordWebhook
import random
import string
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

# Checks required folders are in place
def FolderCheck():

    localDIR = os.path.dirname(os.path.abspath(__file__))
    
    directories = []

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
        exit()

    SendHook(url, content, randomize, times, threader)


if __name__ == "__main__":
    FolderCheck()
    print("\n")
    print(GREEN + "Folder check completed, Launching :)" + RESET)
    time.sleep(0.5)
    Webhooker()