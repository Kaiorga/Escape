# This tool is used to generate the default config file and update settings

import os
import pickle
import resources.tools.helpers as helpers


class GameObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # color uses the Game_Object class
        # background color = x and foreground color = y


def load_config_file():
    try:
        with open('resources/data/config.pickle', 'rb') as config_file:
            grid_size, color, controls, difficulty = pickle.load(config_file)
        config_file.close()
    except FileNotFoundError:
        setup()
        with open('resources/data/config.pickle', 'rb') as config_file:
            grid_size, color, controls, difficulty = pickle.load(config_file)
        config_file.close()
    if helpers.get_os() == 'Windows':
        os.system('color {x}{y}'.format(x=color.x, y=color.y))
    return grid_size, color, controls, difficulty


def write_config_file(grid_size, color, controls, difficulty):
    with open('resources/data/config.pickle', 'wb') as config_file:
        pickle.dump([grid_size, color, controls, difficulty], config_file)
    config_file.close()
    return


def setup():
    print('Could not find config file\nGenerating new config file ...')
    grid_size = GameObject(16, 10)
    color = GameObject('0', '7')
    controls = {'up': 'w', 'left': 'a', 'down': 's', 'right': 'd', 'pause': 'e'}
    difficulty = 0.03125
    write_config_file(grid_size, color, controls, difficulty)
    input('Finished generating config file\nPress ENTER to continue')
    return


def change_grid_size(dimension, old_value):
    print('Enter a new {dimension}\nCurrent {dimension}: {value}'.format(dimension=dimension, value=old_value))
    try:
        new_value = int(input())
        if new_value < 5:
            input('Entered value is to small.'
                  '\nRestoring from config file.\nPress ENTER to continue.'.format(dimension=dimension))
            return old_value
        return new_value
    except ValueError:
        input('ERROR: {dimension} must be an integer.'
              '\nRestoring from config file.\nPress ENTER to continue.'.format(dimension=dimension))
        return old_value


def change_controls(controls):
    print('Current controls')
    for control in controls:
        print('{control}: {key}'.format(control=control, key=controls[control]))
    print('Input new controls')
    for control in controls:
        controls[control] = input('{control}: '.format(control=control))
    return controls


def change_difficulty(difficulty):
    print('Please enter a number between 1 (easy) and 10 (hard).'
          '\nCurrent Difficulty: {difficulty}'.format(difficulty=difficulty * 100))
    try:
        new_difficulty = float(input()) / 100
        if new_difficulty < .01:
            input('ERROR: Number must be greater than 1')
            return difficulty
        if new_difficulty > .1:
            input('ERROR: Number must be less than 10')
            return difficulty
        return new_difficulty
    except ValueError:
        input('ERROR: Difficulty must be a number between 1 and 10')
        return difficulty


def change_color(color):
    print('Pick a new color\nColors'
          '\n0 = Black       8 = Gray\n1 = Blue        9 = Light Blue'
          '\n2 = Green       A = Light Green\n3 = Aqua        B = Light Aqua'
          '\n4 = Red         C = Light Red\n5 = Purple      D = Light Purple'
          '\n6 = Yellow      E = Light Yellow\n7 = White       F = Bright White'
          '\nEntering anything other than one of the colors listed will set colors to default')
    color_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                  'a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D', 'E', 'F']
    background = input('Background Color: ')
    if background not in color_list:
        background = color.x
    foreground = input('Text Color: ')
    if foreground not in color_list:
        foreground = color.y
    if background == foreground:
        input('ERROR: Background and text color cannot be the same.'
              '\nRestoring from config file.\nPress ENTER to continue.')
        background = color.x
        foreground = color.y
    color.x = background
    color.y = foreground
    os.system('color {x}{y}'.format(x=color.x, y=color.y))
    return color


def settings_menu():
    grid_size, color, controls, difficulty = load_config_file()
    while True:
        helpers.clear()
        print('Settings\n\nType the number of an option.\n\n1: Change Grid Length\n2: Change Grid Height'
              '\n3: Change Controls\n4: Change Difficulty')
        if helpers.get_os() == 'Windows':
            print('5: Change Color\n6: Back')
        else:
            print('5: Back')
        option = helpers.get_input()
        helpers.clear()
        if option == '1':
            grid_size.x = change_grid_size('Length', grid_size.x)
        elif option == '2':
            grid_size.y = change_grid_size('Height', grid_size.y - 2) + 2
        elif option == '3':
            controls = change_controls(controls)
        elif option == '4':
            difficulty = change_difficulty(difficulty)
        elif option == '5' and helpers.get_os() == 'Windows':
            color = change_color(color)
        elif option == '5' and helpers.get_os() != 'Windows':
            break
        elif option == '6' and helpers.get_os() == 'Windows':
            break
    write_config_file(grid_size, color, controls, difficulty)
    return grid_size, controls, difficulty
