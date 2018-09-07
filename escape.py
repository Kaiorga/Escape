# Version 5.3.1
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
import resources.tools.highscore as highscore
op_sys = platform.system()
if op_sys == 'Windows':
    import msvcrt as get_key
else:
    import getch as get_key


os.system('title Escape')


class GameObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # color uses the GameObject class
        # background color = x and foreground color = y


def get_input():
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
    global matrix, li, guards
    clear()
    matrix = [[' ' for x in range(grid_size.x)] for y in range(grid_size.y)]
    for sublist in matrix:
        # --top and bottom border--
        g = 0
        while g < grid_size.x:
            matrix[0][g] = '-'
            matrix[grid_size.y-1][g] = '-'
            g += 1
        # --game objects--
        matrix[door][grid_size.x-1] = '}'
        matrix[player.y][player.x] = 'i'
        for guard in guards:
            matrix[guard.y][guard.x] = '#'
        if li is True:
            matrix[life_orb.y][life_orb.x] = '*'
        else:
            matrix[life_orb.y][life_orb.x] = '-'
        # --removes extra characters--
        s = str(sublist)
        s = s.replace('[', '|').replace(']', '|').replace(',', '').replace('\'', '')
        print(s)
    print('Score:', score, 'Lives:', life_count)
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
    global door, player, guards, life_orb, li
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
        li = True
        life_orb = GameObject(random.randint(round(grid_size.x/2), grid_size.x-2), random.randint(1, grid_size.y-2))
    else:
        li = False
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
    global life_orb, li
    life_orb.y = grid_size.y-1
    life_orb.x = grid_size.x-1
    li = False
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
    global game, menu, sv, save_location
    if sv is True:
        os.remove(save_location)
    clear()
    print('Game Over\nScore =', score)
    player = input('Enter a name to go with your score: ')
    if player == '':
        player = '(no name)'
    highscore.update(score, player)
    print('Press "H" to view highscores')
    a = get_input()
    clear()
    if a == 'H' or a == 'h':
        highscore.display()
    game = False
    menu = True
    return


def save():
    global save_location, sv
    try:
        with open(save_location, 'wb') as f:
            pickle.dump([grid_size, score, life_count, life_orb, li, player,
                         guards, door], f)
        clear()
        print('Save Complete')
        input()
        sv = True
    except OSError:
        print('Error: Save Failed\nInvalid file name entered')
        input()


def pause_menu():
    global game, menu, save_location, n
    pause = True
    while pause is True:
        clear()
        print('Type the number of an option.\n\n1: Return to Game\n2: Save\n3: Main Menu')
        n = get_input()
        if n == '1':
            pause = False
        if n == '2':
            clear()
            print('Name this save file\nPress ENTER to use default name')
            save_location = 'resources/save_data/' + input() + '.pickle'
            if save_location == 'resources/save_data/.pickle':
                save_location = 'resources/save_data/svdta.pickle'
            if os.path.isfile(save_location):
                while True:
                    clear()
                    print('WARNING: A save file with that name already exists\nSaving will overwrite the last save game'
                          '\nWould you still like to save the game?\n1: Yes\n2: No')
                    s = get_input()
                    if s == '1':
                        save()
                        break
                    if s == '2':
                        break
            else:
                save()   
        if n == '3':
            pause = False
            menu = True
            game = False
    clear()
    n = False
    grid()
    return


def settings_menu():
    global grid_size, controls
    settings = True
    while settings is True:
        clear()
        print('Settings\n\nType the number of an option.\n\n1: Change grid length\n2: Change grid height'
              '\n3: Change Controls')
        if op_sys == 'Windows':
            print('4: Change Color\n5: Back')
        if op_sys != 'Windows':
            print('4: Back')
        o = get_input()
        clear()
        if o == '1':
            print('Enter a new length\nCurrent length', grid_size.x)
            try:
                xnew = int(input())
            except ValueError:
                xnew = grid_size.x
            if xnew < 10:
                if xnew > 4:
                    print('WARNING: This grid size might not be playable')
                    input()
                if xnew < 5:
                    print('Entered value is to small. Length set to 10')
                    xnew = 10
                    input()
            grid_size.x = xnew
        if o == '2':
            grid_size.y -= 2
            print('Enter a new height\nCurrent height', grid_size.y)
            try:
                ynew = int(input())
            except ValueError:
                ynew = grid_size.y
            if ynew < 8:
                if ynew > 4:
                    print('WARNING: This grid size might not be playable')
                    input()
                if ynew < 5:
                    print('Entered value is to small. Height set to 8')
                    ynew = 8
                    input()
            grid_size.y = ynew + 2
        if o == '3':
            print('Current controls')
            for control in controls:
                print(control + ':', controls[control])
            print('Input new controls')
            for control in controls:
                new_input = input(control + ': ')
                controls[control] = new_input
        if o == '4' and op_sys == 'Windows':
            print('Pick a new color\nColors\n0 = Black       8 = Gray\n1 = Blue        9 = Light Blue\n2 = Green       '
                  'A = Light Green\n3 = Aqua        B = Light Aqua\n4 = Red         C = Light Red\n5 = Purple      '
                  'D = Light Purple\n6 = Yellow      E = Light Yellow\n7 = White       F = Bright White'
                  '\nEntering anything other than one of the colors listed will set colors to default')
            color_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                          'a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D', 'E', 'F']
            print('Background Color')
            background = input()
            if background not in color_list:
                background = color.x
            print('Text Color')
            foreground = input()
            if foreground not in color_list:
                foreground = color.y
            if background == foreground:
                print('ERROR: Background and text color cannot be the same.'
                      '\nRestoring from config file.\nPress ENTER to continue.')
                input()
                background = color.x
                foreground = color.y
            color.x = background
            color.y = foreground
            os.system('color ' + color.x + color.y)
        if o == '4' and op_sys != 'Windows':
            settings = False
        if o == '5' and op_sys == 'Windows':
            settings = False
    with open('resources/data/config.pickle', 'wb') as config_file:
                    pickle.dump([grid_size, color, controls], config_file)
    return


# --master loop--
try:
    with open('resources/data/config.pickle', 'rb') as config_file:
        grid_size, color, controls = pickle.load(config_file)
except FileNotFoundError:
    config.setup('resources/data/config.pickle', 'continue')
    with open('resources/data/config.pickle', 'rb') as config_file:
        grid_size, color, controls = pickle.load(config_file)
os.system('color ' + color.x + color.y)
master = True
menu = True
game = False
while master is True:
    # --menu loop--
    while menu is True:
        clear()
        print('Type the number of an option.\n\n1: New Game\n2: Load Game'
              '\n3: Highscore\n4: Instructions\n5: Settings\n6: Quit')
        m = get_input()
        clear()
        if m == '1':
            menu = False
            game = True
            sv = False
            life_count = 1
            score = 0
            new_round()
        if m == '2':
            print('Type in the name of the save file.\nPress ENTER to use the defualt save file')
            save_location = 'resources/save_data/' + input() + '.pickle'
            if save_location == 'resources/save_data/.pickle':
                save_location = 'resources/save_data/svdta.pickle'
            try:
                with open(save_location, 'rb') as svdta:
                    grid_size, score, life_count, life_orb, li, player,\
                        guards, door = pickle.load(svdta)
                menu = False
                game = True
                sv = True
                grid()
            except FileNotFoundError:
                print('No save data found')
                input()
            except OSError:
                print('Error: Load Failed\nInvalid file name entered')
                input()
                
        if m == '3':
            highscore.display()
        if m == '4':
            print('Instructions\n\nGet your person (i) to the exit (})\nwithout getting caught by the guards (#).'
                  '\n(*) will give you +1 life.\nUse the \'' + controls['up'] + '\',\'' + controls['left'] + '\',\'' +
                  controls['down'] + '\',\'' + controls['right'] + '\' keys to move your character.'
                  '\nUse the \'' + controls['pause'] + '\' key to open the pause menu.')
            input()
        if m == '5':
            settings_menu()
        if m == '6':
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
