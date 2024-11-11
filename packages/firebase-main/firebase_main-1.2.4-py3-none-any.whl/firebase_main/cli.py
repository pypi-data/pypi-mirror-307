import subprocess
import sys
import os
import time
from colorama import init, Fore
from trackdir import track_changes
import argparse
init(autoreset=True)

def check_command_exists(command):
    if os.name == 'nt':  
        check_cmd = "where"
    elif sys.platform == 'darwin' or sys.platform == 'linux':  
        check_cmd = "command -v"
    else:
        raise Exception("Unsupported OS")
    result = subprocess.run(f"{check_cmd} {command}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

def check_firebase_cli():
    if check_command_exists("firebase"):
        pass
    else:
        print(f"{Fore.YELLOW}Firebase CLI not found. Attempting to install...{Fore.RESET}")
        if not check_command_exists("node"):
            print(f"{Fore.RED}Node.js is required for Firebase CLI but is not installed. Please install Node.js first.{Fore.RESET}")
            print("Visit https://nodejs.org/ for installation.")
            sys.exit(1)
        if not check_command_exists("npm"):
            print(f"{Fore.RED}npm is required to install Firebase CLI but is not installed. Please install npm on your system first.{Fore.RESET}")
            print("Visit https://www.npmjs.com/get-npm for installation.")
            sys.exit(1)
        try:
            print(f"{Fore.YELLOW}Installing Firebase CLI...{Fore.RESET}")
            os.system("npm install -g firebase-tools")
            if check_command_exists("firebase"):
                print(f"{Fore.GREEN}Firebase CLI installed successfully.{Fore.RESET}")
            else:
                raise Exception("Firebase CLI installation failed.")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Installation interrupted. Exiting...{Fore.RESET}")
            sys.exit(1)
        except Exception as e:
            print(f"{Fore.RED}Failed to install Firebase CLI: {e}{Fore.RESET}")
            print(f"{Fore.RED}Please install it manually using the command: npm install -g firebase-tools{Fore.RESET}")
            sys.exit(1)

def check_node():
    if check_command_exists("node"):
        pass
    else:
        print(f"{Fore.RED}Node.js is required but not installed. Please install it from https://nodejs.org/.{Fore.RESET}")
        sys.exit(1)

def firebase_deploy():
    print(f"{Fore.CYAN}Starting Firebase deploy...{Fore.RESET}")
    os.system("firebase deploy")

def firebase_init():
    print(f"{Fore.CYAN}Initializing Firebase project...{Fore.RESET}")
    os.system("firebase init")

def firebase_disable_hosting():
    print(f"{Fore.CYAN}Disabling Firebase Hosting...{Fore.RESET}")
    os.system("firebase hosting:disable")

def show_functions_log():
    print(f"{Fore.CYAN}Displaying Firebase Functions log...{Fore.RESET}")
    os.system("firebase functions:log")

def firebase_help():
    print(f"{Fore.CYAN}Showing Firebase help...{Fore.RESET}")
    os.system("firebase --help")

def firebase_login():
    print(f"{Fore.CYAN}Logging into Firebase...{Fore.RESET}")
    os.system("firebase login")

def firebase_logout():
    print(f"{Fore.CYAN}Logging out of Firebase...{Fore.RESET}")
    os.system("firebase logout")

def track_and_deploy(directory):
    print(f"{Fore.CYAN}Tracking changes in directory: {directory}{Fore.RESET}")
    while True:
        change = track_changes(directory)
        if change:
            event_type = change["type"]
            event_path = change["path"]
            if event_type == 'modified':
                print(f"File modified: {event_path}")
            elif event_type == 'created':
                print(f"File created: {event_path}")
            elif event_type == 'deleted':
                print(f"File deleted: {event_path}")
            print(f"{Fore.CYAN}Change detected, deploying to Firebase...{Fore.RESET}")
            firebase_deploy()
        time.sleep(1)

def main():
    parser = argparse.ArgumentParser(description="Firebase CLI Management Tool")
    parser.add_argument("command", nargs="?", choices=["deploy", "init", "login", "logout", "disable", "functions-log", "help", "track", "track-deploy"],
                        help="The command to run")
    args = parser.parse_args()

    check_node()
    check_firebase_cli()

    if not args.command:
        directory_to_track = os.getcwd()
        print(f"{Fore.CYAN}######## #### ########  ######## ########     ###     ######  ########{Fore.RESET}")
        print(f"{Fore.CYAN}##        ##  ##     ## ##       ##     ##  ##   ##  ##       ##{Fore.RESET}")
        print(f"{Fore.CYAN}######    ##  ########  ######   ########  #########  ######  ######{Fore.RESET}")
        print(f"{Fore.CYAN}##        ##  ##    ##  ##       ##     ## ##     ##       ## ##{Fore.RESET}")
        print(f"{Fore.CYAN}##       #### ##     ## ######## ########  ##     ##  ######  ########{Fore.RESET}")
        print("")
        while True:
            print(f"{Fore.WHITE}[{Fore.GREEN}01{Fore.WHITE}] Deploy{Fore.RESET}")
            print(f"{Fore.WHITE}[{Fore.GREEN}02{Fore.WHITE}] Init{Fore.RESET}")
            print(f"{Fore.WHITE}[{Fore.GREEN}03{Fore.WHITE}] Disable Hosting{Fore.RESET}")
            print(f"{Fore.WHITE}[{Fore.GREEN}04{Fore.WHITE}] Show Functions Log{Fore.RESET}")
            print(f"{Fore.WHITE}[{Fore.GREEN}06{Fore.WHITE}] Start Live Tracking and Deploy{Fore.RESET}")
            print(f"{Fore.WHITE}[{Fore.GREEN}07{Fore.WHITE}] Login{Fore.RESET}")
            print(f"{Fore.WHITE}[{Fore.GREEN}08{Fore.WHITE}] Help{Fore.RESET}")
            print(f"{Fore.WHITE}[{Fore.RED}09{Fore.WHITE}] Logout{Fore.RESET}")
            print(f"{Fore.WHITE}[{Fore.RED}10{Fore.WHITE}] Exit{Fore.RESET}")
            try:
                choice = input(f"{Fore.GREEN}Choose an option: {Fore.RESET}")
                if choice == "1" or choice == "01":
                    firebase_deploy()
                elif choice == "2" or choice == "02":
                    firebase_init()
                elif choice == "3" or choice == "03":
                    firebase_disable_hosting()
                elif choice == "4" or choice == "04":
                    show_functions_log()
                elif choice == "6" or choice == "06":
                    print(f"{Fore.CYAN}Starting live tracking and deploy...{Fore.RESET}")
                    track_and_deploy(directory_to_track)
                elif choice == "7" or choice == "07":
                    firebase_login()
                elif choice == "8" or choice == "08":
                    firebase_help()
                elif choice == "9" or choice == "09":
                    firebase_logout()
                elif choice == "10":
                    print(f"{Fore.YELLOW}Exiting...{Fore.RESET}")
                    break
                else:
                    print(f"{Fore.RED}Invalid choice. Please try again.{Fore.RESET}")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Exiting...{Fore.RESET}")
                break
    else:
        if args.command == "deploy":
            firebase_deploy()
        elif args.command == "init":
            firebase_init()
        elif args.command == "disable":
            firebase_disable_hosting()
        elif args.command == "functions-log":
            show_functions_log()
        elif args.command == "help":
            firebase_help()
        elif args.command == "login":
            firebase_login()
        elif args.command == "logout":
            firebase_logout()
        elif args.command == "track-deploy":
            track_and_deploy(args.directory)
        else:
            print(f"{Fore.RED}Invalid command. Please try again.{Fore.RESET}")

if __name__ == "__main__":
    main()
