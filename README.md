# Rixin

Rixin is a collection of tools created as a summer project. It was created and tested on windows, tools will work on other OS' but may have bugs. Either version will generate new folders in the directory to allow for things like templates and storing details.

## Preview
![ModulePreview](https://github.com/user-attachments/assets/b2dcd7e7-69ae-4d6c-bc6d-cd1b47a0d0c8)

## Features

- Gmail SMTP Sender: The SMTP sender is able to send emails to a selected email adress from a gmail account with a valid app password. After running it will create the needed folders including templates and logins. Store your selected login details in the format 'email@gmail.com:app_password' in a text document in the logins folder and the tool will give you the ability to login.

- Qr-Code Generator: The Qr-Code generator uses pythons 'qrcode' library to generate a qr-code to a selected URL. It gives the user the ability to save the new image to a default folder or a selected folder.

- Discord Webhook Sender: Enter a discord webhook URL and send messages through it using pythons 'discord_webhook' library. You can specify the amount of times to send the message.

## Usage

The Modular version: Each tool is in its own folder allowing for easier editing and better running on machines.

To use the Modular version either run:
```bash
cd Rixin-Modules
python RIXIN.py
```
Or enter the specific directory for each tool and run its own python file e.g:
```bash
python QRGEN.py
python SMTP.py
python WEBHOOK.py
```

## Contributing
Contributions are welcome! Feel free to submit a pull request or open an issue if you have suggestions or find bugs.

## License
This project is licensed under the GPL v3 License - see the LICENSE file for details.

## Acknowledgments
Created by Areeves.
Just a student looking for something to do.

## Installation

To get started with Rixin, clone this repository and install the necessary dependencies.

```bash
git clone https://github.com/Ar-eeves/rixin.git
cd rixin
pip install -r requirements.txt
```
