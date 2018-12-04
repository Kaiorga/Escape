# Version 5.4.1
# Escape by TyReesh Boedhram
# NOTE: This game must be run in Command Prompt on Windows or Terminal on Linux to work properly.
# This game will not work properly in IDLE.
# Not tested on Mac OSX yet.
# Please report any bugs.

import os
import pickle
import random
import platform
import resources.tools.config as config
from resources.tools.config import GameObject
import resources.tools.highscore as highscore
op_sys = platform.system()
if op_sys == 'Windows':
    import msvcrt as get_key
else:
    import getch as get_key


os.system('title Escape')


def get_input(message=''):
    if message != '':
        print(message)
    if op_sys == 'Windows':
        user_input = str(get_key.getch())
        user_input = user_input.replace('b', '').replace('\'', '')
        return user_input
    else:
        return str(get_key.getch())


def clear():
    if op_sys == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    return


def grid():
    global matrix, life_orb_active, guards
    clear()
    matrix = [[' ' for _ in range(grid_size.x)] for _ in range(grid_size.y)]
#   --top and bottom border--
    column = 0
    while column < grid_size.x:
        matrix[0][column] = '-'
        matrix[grid_size.y-1][column] = '-'
        column += 1
#   --game objects--
    matrix[door][grid_size.x-1] = '}'
    matrix[player.y][player.x] = 'i'
    for guard in guards:
        matrix[guard.y][guard.x] = '#'
    if life_orb_active:
        matrix[life_orb.y][life_orb.x] = '*'
    else:
        matrix[life_orb.y][life_orb.x] = '-'
#   --removes extra characters--
    for row in matrix:
        row_string = str(row)
        row_string = row_string.replace('[', '|').replace(']', '|').replace(',', '').replace('\'', '')
        print(row_string)
    print('Score: {score}\tLives: {lives}'.format(score=score, lives=life_count))
    return


# --Player Commands--
def player_input():
    global player
    y = get_input()
    if y == controls['up'] and player.y > 1:
        player.y -= 1
    if y == controls['left'] and player.x > 0:
        player.x -= 1
    if y == controls['down'] and player.y < grid_size.y-2:
        player.y += 1
    if y == controls['right'] and player.x < grid_size.x-1:
        player.x += 1
        if player.y != door and player.x == grid_size.x-1:
            player.x -= 1
    if y == controls['pause']:
        pause_menu()
    return


# --Guard Movement AI--
def ai():
    global guards
    for guard in guards:
        direction = random.randint(1, 4)
        if direction == 1 and guard.y > 1:
            guard.y -= 1
        if direction == 2 and guard.x < grid_size.x-2:
            guard.x += 1
        if direction == 3 and guard.y < grid_size.y-2:
            guard.y += 1
        if direction == 4 and guard.x > 0:
            guard.x -= 1


def new_round():
    global door, player, guards, life_orb, life_orb_active
    door = random.randint(1, grid_size.y-2)
    player = GameObject(0, random.randint(1, grid_size.y-2))
    number_of_guards = round((grid_size.x * (grid_size.y - 2)) / (grid_size.x + (grid_size.y - 2)))
    guards = []
    index = 0
    while index < number_of_guards:
        guard = GameObject(random.randint(2, grid_size.x-2), random.randint(1, grid_size.y-2))
        guards.append(guard)
        index += 1
    if random.randint(1, 5) == 3:
        life_orb_active = True
        life_orb = GameObject(random.randint(round(grid_size.x/2), grid_size.x-2), random.randint(1, grid_size.y-2))
    else:
        life_orb_active = False
        life_orb = GameObject(grid_size.x-1, grid_size.y-1)
    grid()
    return


def life():
    global life_count
    life_count += 1
    if life_count > 10:
        life_count = 10
    return


def life_2():
    global life_orb, life_orb_active
    life_orb.y = grid_size.y-1
    life_orb.x = grid_size.x-1
    life_orb_active = False
    grid()
    return


def end_round():
    global life_count
    life_count -= 1
    if life_count == 0:
        end_game()
    else:
        new_round()
    return


def end_game():
    global game, menu, save_active, save_location
    if save_active:
        os.remove(save_location)
    clear()
    player = input('Game Over\nScore: {score}\nEnter a name to go with your score: '.format(score=score))
    if player == '':
        player = '(no name)'
    highscore.update(score, player, grid_size)
    a = get_input('Press "H" to view highscores')
    clear()
    if a == 'H' or a == 'h':
        highscore.display(grid_size)
    game = False
    menu = True
    return


def save():
    global save_location, save_active
    try:
        with open(save_location, 'wb') as f:
            pickle.dump([grid_size, score, life_count, life_orb, life_orb_active, player,
                         guards, door], f)
        clear()
        input('Save Complete')
        save_active = True
    except OSError:
        input('Error: Save Failed\nInvalid file name entered')


def pause_menu():
    global game, menu, save_location, n
    while True:
        clear()
        option = get_input('Type the number of an option.\n\n1: Return to Game\n2: Save\n3: Main Menu')
        if option == '1':
            break
        if option == '2':
            clear()
            print('Name this save file\nPress ENTER to use default name')
            save_location = 'resources/save_data/{name}.pickle'.format(name=input())
            if save_location == 'resources/save_data/.pickle':
                save_location = 'resources/save_data/svdta.pickle'
            if os.path.isfile(save_location):
                while True:
                    clear()
                    s = get_input('WARNING: A save file with that name already exists\n'
                                  'Saving will overwrite the last save game\n'
                                  'Would you still like to save the game?\n1: Yes\n2: No')
                    if s == '1':
                        save()
                        break
                    if s == '2':
                        break
            else:
                save()   
        if option == '3':
            menu = True
            game = False
            break
    clear()
    n = False
    grid()
    return


def settings_menu():
    global grid_size, controls
    while True:
        clear()
        print('Settings\n\nType the number of an option.\n\n1: Change grid length\n2: Change grid height'
              '\n3: Change Controls')
        if op_sys == 'Windows':
            print('4: Change Color\n5: Back')
        if op_sys != 'Windows':
            print('4: Back')
        option = get_input()
        clear()
        if option == '1':
            print('Enter a new length\nCurrent length {length}'.format(length=grid_size.x))
            try:
                x_new = int(input())
            except ValueError:
                input('ERROR: Length must be an integer.'
                      '\nRestoring from config file.\nPress ENTER to continue.')
                x_new = grid_size.x
            if x_new < 10:
                if x_new > 4:
                    input('WARNING: This grid size might not be playable')
                if x_new < 5:
                    input('Entered value is to small. Length set to 10')
                    x_new = 10
            grid_size.x = x_new
        if option == '2':
            grid_size.y -= 2
            print('Enter a new height\nCurrent height {height}'.format(height=grid_size.y))
            try:
                y_new = int(input())
            except ValueError:
                input('ERROR: Height must be an integer.'
                      '\nRestoring from config file.\nPress ENTER to continue.')
                y_new = grid_size.y
            if y_new < 8:
                if y_new > 4:
                    input('WARNING: This grid size might not be playable')
                if y_new < 5:
                    input('Entered value is to small. Height set to 8')
                    y_new = 8
            grid_size.y = y_new + 2
        if option == '3':
            print('Current controls')
            for control in controls:
                print('{control}: {key}'.format(control=control, key=controls[control]))
            print('Input new controls')
            for control in controls:
                controls[control] = input('{control}: '.format(control=control))
        if option == '4' and op_sys == 'Windows':
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
        else:
            break
        if option == '5' and op_sys == 'Windows':
            break
    with open('resources/data/config.pickle', 'wb') as config_file:
                    pickle.dump([grid_size, color, controls], config_file)
    return


# --master loop--
try:
    with open('resources/data/config.pickle', 'rb') as config_file:
        grid_size, color, controls = pickle.load(config_file)
except FileNotFoundError:
    config.setup('resources/data/config.pickle')
    with open('resources/data/config.pickle', 'rb') as config_file:
        grid_size, color, controls = pickle.load(config_file)
os.system('color {x}{y}'.format(x=color.x, y=color.y))
master = True
menu = True
game = False
while master is True:
    # --menu loop--
    while menu is True:
        clear()
        option = get_input('Type the number of an option.\n\n1: New Game\n2: Load Game'
                      '\n3: Highscore\n4: Instructions\n5: Settings\n6: Quit')
        clear()
        if option == '1':
            menu = False
            game = True
            save_active = False
            life_count = 1
            score = 0
            new_round()
        if option == '2':
            print('Type in the name of the save file.\nPress ENTER to use the defualt save file')
            save_location = 'resources/save_data/{name}.pickle'.format(name=input())
            if save_location == 'resources/save_data/.pickle':
                save_location = 'resources/save_data/svdta.pickle'
            try:
                with open(save_location, 'rb') as svdta:
                    grid_size, score, life_count, life_orb, life_orb_active, player,\
                        guards, door = pickle.load(svdta)
                menu = False
                game = True
                save_active = True
                grid()
            except FileNotFoundError:
                input('No save file found')
            except OSError:
                input('Error: Load Failed\nInvalid file name entered')
                
        if option == '3':
            highscore.display(grid_size)
        if option == '4':
            input('Instructions\n\n'
                  'Get your person (i) to the exit ({door})\n'
                  'without getting caught by the guards (#).\n'
                  '(*) will give you +1 life.\n'
                  'Use the \'{up}\',\'{left}\',\'{down}\',\'{right}\' keys to move your character.\n'
                  'Use the \'{pause}\' key to open the pause menu.'.format(door='}', up=controls['up'],
                                                                           left=controls['left'], down=controls['down'],
                                                                           right=controls['right'], pause=controls['pause']))
        if option == '5':
            settings_menu()
        if option == '6':
            master = False
            menu = False
            game = False

    # --game loop--
    while game is True:
        n = True
        player_input()
        if n is True:
            ai()
            grid()
        if player.y == door and player.x == grid_size.x-1:
            score += 1
            new_round()
        if player.y == life_orb.y and player.x == life_orb.x:
            life()
            life_2()
        for guard in guards:
            if life_orb.y == guard.y and life_orb.x == guard.x:
                life_2()
            if player.y == guard.y and player.x == guard.x:
                end_round()
            if player.y == guard.y and player.x == guard.x-1:
                end_round()
            if player.y == guard.y and player.x == guard.x+1:
                end_round()
            if player.y == guard.y-1 and player.x == guard.x:
                end_round()
            if player.y == guard.y+1 and player.x == guard.x:
                end_round()
