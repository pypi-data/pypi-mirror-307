import os
import sys
from colorama import init, Fore
from trackdir import track_changes

init(autoreset=True)

def show_banner():
    banner = """
######## #### ########  ######## ########     ###     ######  ########
##        ##  ##     ## ##       ##     ##  ##   ##  ##       ##
######    ##  ########  ######   ########  #########  ######  ######
##        ##  ##    ##  ##       ##     ## ##     ##       ## ##
##       #### ##     ## ######## ########  ##     ##  ######  ########
    """
    print(Fore.CYAN + banner + Fore.RESET)

def track_directory(directory_to_track):
    print(f"{Fore.YELLOW}Tracking changes in directory: {directory_to_track}{Fore.RESET}")
    change = track_changes(directory_to_track)
    if change:
        event_type = change["type"]
        event_path = change["path"]
        if event_type == 'modified':
            print(f"{Fore.GREEN}File modified: {event_path}{Fore.RESET}")
        elif event_type == 'created':
            print(f"{Fore.CYAN}File created: {event_path}{Fore.RESET}")
        elif event_type == 'deleted':
            print(f"{Fore.RED}File deleted: {event_path}{Fore.RESET}")

def firebase_login():
    os.system("firebase login")

def firebase_logout():
    os.system("firebase logout")

def firebase_deploy():
    os.system("firebase deploy")

def firebase_init():
    os.system("firebase init")

def disable_hosting():
    os.system("firebase hosting:disable")

def show_functions_log():
    os.system("firebase functions:log")

def show_menu():
    print(f"{Fore.WHITE}[{Fore.GREEN}01{Fore.WHITE}] Deploy{Fore.RESET}")
    print(f"{Fore.WHITE}[{Fore.GREEN}02{Fore.WHITE}] Init{Fore.RESET}")
    print(f"{Fore.WHITE}[{Fore.GREEN}03{Fore.WHITE}] Disable Hosting{Fore.RESET}")
    print(f"{Fore.WHITE}[{Fore.GREEN}04{Fore.WHITE}] Show Functions Log{Fore.RESET}")
    print(f"{Fore.WHITE}[{Fore.GREEN}05{Fore.WHITE}] Help{Fore.RESET}")
    print(f"{Fore.WHITE}[{Fore.GREEN}08{Fore.WHITE}] Track and Live Deploy{Fore.RESET}")
    print(f"{Fore.WHITE}[{Fore.GREEN}07{Fore.WHITE}] Login{Fore.RESET}")
    print(f"{Fore.WHITE}[{Fore.GREEN}08{Fore.WHITE}] Logout{Fore.RESET}")
    print(f"{Fore.WHITE}[{Fore.RED}09{Fore.WHITE}] Exit{Fore.RESET}")

def main():
    logged_in = False
    directory_to_track = os.getcwd()  

    show_banner()

    while True:
        try:
            show_menu()
            choice = input(f"{Fore.GREEN}Choose an option: {Fore.RESET}")

            if choice == "1" or choice == "01":
                firebase_deploy()
            elif choice == "2" or choice == "02":
                firebase_init()
            elif choice == "3" or choice == "03":
                disable_hosting()
            elif choice == "4" or choice == "04":
                show_functions_log()
            elif choice == "5" or choice == "05":
                print("Help: This tool helps you manage Firebase commands like deploy, init, etc.")
            elif choice == "7" or choice == "07":
                if not logged_in:
                    firebase_login()
                    logged_in = True
                else:
                    print("Already logged in.")
            elif choice == "8" or choice == "08":
                if logged_in:
                    firebase_logout()
                    logged_in = False
                else:
                    print("Not logged in.")
            elif choice == "9" or choice == "09":
                print("Exiting...")
                sys.exit()
            elif choice == "8" or choice == "08":
                print("Tracking changes in directory...")
                track_directory(directory_to_track)
            else:
                print(f"{Fore.RED}[ERROR] Invalid choice or not logged in. Please try again.{Fore.RESET}")

        except KeyboardInterrupt:
            print(f"\n{Fore.RED}Program interrupted. Exiting...{Fore.RESET}")
            sys.exit()

if __name__ == "__main__":
    main()
