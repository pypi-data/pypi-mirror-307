# Firebase Main CLI Tool

`firebase-main` is a command-line tool that simplifies the management of Firebase projects. It allows you to deploy, initialize, manage hosting, view function logs, track file changes, and handle login/logout for Firebase directly from the terminal.

## Features

- **Deploy** Firebase project
- **Initialize** Firebase project
- **Disable Hosting** on Firebase
- **Show Functions Log** for Firebase functions
- **Track File Changes** in the current working directory
- **Login/Logout** with Firebase
- **Help**: Provides help information on using the tool
- **Track Directory Changes**: Monitor files for changes (created, modified, deleted)

## Installation

To install `firebase-main`, you can use `pip`:

```bash
pip install firebase-main
```

Ensure you have Python and Firebase CLI installed on your system before using this tool.

### Prerequisites

- Python 3.6+
- Firebase CLI: [Install Firebase CLI](https://firebase.google.com/docs/cli#install_the_firebase_cli)
- Install the required dependencies for the Firebase CLI: `npm install -g firebase-tools`

## Usage

After installation, you can use the tool by running `firebase-main` from your terminal. Below are the available commands:

### Options:
```
[01] Deploy Firebase Project  
[02] Initialize Firebase Project 
[03] Disable Hosting 
[04] Show Functions Log
[05] Help 
[08] Track and Live Deploy
[07] Login to Firebase  
[08] Logout from Firebase
[09] Exit
```

### Command Descriptions:

1. **Deploy Firebase Project**  
   Deploys your Firebase project to Firebase Hosting.

2. **Initialize Firebase Project**  
   Initializes a Firebase project in your current directory.

3. **Disable Hosting**  
   Disables Firebase Hosting for your project.

4. **Show Functions Log**  
   Displays the logs of Firebase Functions.

5. **Help**  
   Provides details on how to use the tool.

6. **Track and Live Deploy**  
   Tracks file changes in your project directory and live deploys updates.

7. **Login**  
   Logs you into Firebase. Once logged in, you don’t need to log in again unless you log out.

8. **Logout**  
   Logs you out of Firebase.

9. **Exit**  
   Exits the tool.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to fork the repository, submit issues, or create pull requests.

## Acknowledgments

- [Firebase](https://firebase.google.com/) - Platform for building mobile and web applications.

---

Made with 💖 by **ByteBreach**.
