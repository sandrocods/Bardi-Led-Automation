import time
import os
from src.BardiHelper import BardiConnector
import inquirer
from colorama import Fore, init
from alive_progress import alive_bar

init(autoreset=True)

print(Fore.GREEN + """
   ___               _ _     __          _     _         _                        _   _             
  / __\ __ _ _ __ __| (_)   / /  ___  __| |   /_\  _   _| |_ ___  _ __ ___   __ _| |_(_) ___  _ __  
 /__\/// _` | '__/ _` | |  / /  / _ \/ _` |  //_\\| | | | __/ _ \| '_ ` _ \ / _` | __| |/ _ \| '_ \ 
/ \/  \ (_| | | | (_| | | / /__|  __/ (_| | /  _  \ |_| | || (_) | | | | | | (_| | |_| | (_) | | | |
\_____/\__,_|_|  \__,_|_| \____/\___|\__,_| \_/ \_/\__,_|\__\___/|_| |_| |_|\__,_|\__|_|\___/|_| |_|
 Code by @sandrocods                                                                                              
""")


def menu(connector_bardi=None, sleep_condition=None):
    os.system('cls')
    print(Fore.GREEN + "[!] Connected to device: {}".format(connector_bardi.device_name))

    if sleep_condition:
        connector_bardi.sleep_device(status=True)
        questions_wake = [
            inquirer.List('wake',
                          message="Wake device?",
                          choices=['Yes', 'No'],
                          ),
        ]
        answers_wake = inquirer.prompt(questions_wake)
        if answers_wake['wake'] == 'Yes':
            connector_bardi.sleep_device(status=False)
            time.sleep(1)
            menu(connector_bardi=connector_bardi, sleep_condition=False)
        else:
            menu(connector_bardi=connector_bardi, sleep_condition=True)

    else:

        questions_menu = [
            inquirer.List('menu',
                          message="What do you want to do?",
                          choices=[
                              'Sleep Phone',
                              'Change Color LED',
                              'Change Theme LED',
                              'Change Power Device',
                              'Change Brightness LED',
                              'Exit'],
                          ),
        ]
        answers_menu = inquirer.prompt(questions_menu)
        if answers_menu['menu'] == 'Change Color LED':

            questions_color = [
                inquirer.List('color',
                              message="What color do you want to set?",
                              choices=connector_bardi.location_color,
                              ),
            ]
            answers_color = inquirer.prompt(questions_color)
            connector_bardi.change_color(answers_color['color'])
            menu(connector_bardi)

        elif answers_menu['menu'] == 'Change Brightness LED':

            questions_brightness = [
                inquirer.List('brightness',
                              message="What brightness do you want to set?",
                              choices=connector_bardi.brightness,
                              ),
            ]
            answers_brightness = inquirer.prompt(questions_brightness)
            connector_bardi.change_brightness(answers_brightness['brightness'])
            menu(connector_bardi)

        elif answers_menu['menu'] == 'Change Theme LED':

            questions_theme = [
                inquirer.List('theme',
                              message="What theme do you want to set?",
                              choices=["Music", "Normal"],
                              ),
            ]
            answers_theme = inquirer.prompt(questions_theme)
            if answers_theme['theme'] == "Music":

                connector_bardi.get_theme_by_music()

                questions_theme_music = [
                    inquirer.List('theme_music',
                                  message="What theme music do you want to set?",
                                  choices=connector_bardi.theme_data,
                                  ),
                ]
                answers_theme_music = inquirer.prompt(questions_theme_music)

                connector_bardi.change_theme(theme_name=answers_theme_music['theme_music']['theme_name'],
                                             theme_type="music")
                del connector_bardi.theme_data
                menu(connector_bardi)
            else:

                connector_bardi.get_theme()
                questions_theme_normal = [
                    inquirer.List('theme_normal',
                                  message="What theme normal do you want to set?",
                                  choices=connector_bardi.theme_data,
                                  ),
                ]
                answers_theme_normal = inquirer.prompt(questions_theme_normal)

                connector_bardi.change_theme(theme_name=answers_theme_normal['theme_normal']['theme_name'],
                                             theme_type="normal")
                del connector_bardi.theme_data
                menu(connector_bardi)

        elif answers_menu['menu'] == 'Change Power Device':

            questions_power = [
                inquirer.List('power',
                              message="What power do you want to set?",
                              choices=['on', 'off'],
                              ),
            ]
            answers_power = inquirer.prompt(questions_power)
            connector_bardi.change_state(answers_power['power'])
            menu(connector_bardi)

        elif answers_menu['menu'] == 'Sleep Phone':
            menu(connector_bardi, sleep_condition=True)

        elif answers_menu['menu'] == 'Exit':
            exit()


global connector_bardi
questions_connection = [
    inquirer.List('connection_type',
                  message="Select connection type",
                  choices=['usb', 'wifi', 'ngrok'],
                  ),
]

answers_connection = inquirer.prompt(questions_connection)
if answers_connection["connection_type"] == "wifi":
    questions_wifi = [
        inquirer.Text('address',
                      message="Enter address",
                      ),
    ]

    connector_bardi = BardiConnector(
        timeout=10.0,
        connection_type="wifi",
        address=inquirer.prompt(questions_wifi)["address"]
    )

elif answers_connection["connection_type"] == "usb":
    connector_bardi = BardiConnector(
        timeout=10.0,
        connection_type="usb",
    )

elif answers_connection["connection_type"] == "ngrok":

    questions_ngrok = [
        inquirer.Text('address',
                      message="Enter address",
                      ),
    ]
    connector_bardi = BardiConnector(
        timeout=10.0,
        connection_type="ngrok",
        address=inquirer.prompt(questions_ngrok)["address"]
    )

get_device_bardi = connector_bardi.get_bardi_device()
if get_device_bardi["status"]:
    with alive_bar(total=len(get_device_bardi["data_device"]), title="Get Device Bardi", force_tty=True) as bar:
        for device in get_device_bardi["data_device"]:
            bar()
            time.sleep(0.5)

    questions_device = [
        inquirer.List('device',
                      message="Select device",
                      choices=get_device_bardi["data_device"],
                      ),
    ]

    answers_device = inquirer.prompt(questions_device)["device"]

    connect_device_bardi = connector_bardi.connect_bardi_device(answers_device)
    if connect_device_bardi["status"]:
        print(Fore.GREEN + "[!] Device {} connected".format(answers_device))
        menu(
            connector_bardi=connector_bardi,
        )

    else:
        print(Fore.RED + "[!] Device not connected")

else:
    print(Fore.RED + "[!] Device not found")
