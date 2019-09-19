# This file contains helper functions.

import os
import platform
OS = platform.system()
if OS == 'Windows':
    import msvcrt as get_key
else:
    import getch as get_key


def get_os():
    return OS


def get_input(message=''):
    # return input(message)
    if message != '':
        print(message)
    if get_os() == 'Windows':
        user_input = str(get_key.getch())
        user_input = user_input.replace('b', '').replace('\'', '')
        return user_input
    else:
        return str(get_key.getch())


def clear():
    if get_os() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    return
