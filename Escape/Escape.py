#Version 4.0.2
#Escape by TyReesh Boedhram
#NOTE: This game must be run in Command Prompt on Windows or Terminal in Linux to work properly.
#This game will not work properly on Sololearn or in IDLE.
#Not tested on Mac OSX yet.
#Please report any bugs.

import os
import pickle
import random
import platform

os.system('title Escape')
op_sys = platform.system()

class Game_Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #color uses the Game_Object class
        #background color = x and forground color = y

def clear():
    if op_sys == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    return

def grid():
    global matrix, li
    clear()
    matrix = [[ ' ' for x in range(gridSize.x)] for y in range(gridSize.y)]
    for sublist in matrix:
        #--top and bottom border--
        g = 0
        while g < gridSize.x:
            matrix[0][g] = '-'
            matrix[gridSize.y-1][g] = '-'
            g += 1
        #--game objects--
        matrix[door][gridSize.x-1] = '}'
        matrix[player.y][player.x] = 'i'
        matrix[guard1.y][guard1.x] = '#'
        matrix[guard2.y][guard2.x] = '#'
        matrix[guard3.y][guard3.x] = '#'
        matrix[guard4.y][guard4.x] = '#'
        if li == True:
            matrix[lifeOrb.y][lifeOrb.x] = '*'
        else:
            matrix[lifeOrb.y][lifeOrb.x] = '-'
        #--removes extra characters--
        s = str(sublist)
        s = s.replace('[', '|').replace(']', '|').replace(',','').replace('\'','')
        print (s)
    print ('Score:',score,'Lives:',lifeCount)
    return

#--Player Commands--
def Player():
    global player
    Y = input()
    if Y == 'w' and player.y > 1:
        player.y -= 1
    if Y == 'a' and player.x > 0:
        player.x -= 1
    if Y == 's' and player.y < gridSize.y-2:
        player.y += 1
    if Y == 'd' and player.x < gridSize.x-1:
        player.x += 1
        if player.y != door and player.x == gridSize.x-1:
            player.x -= 1
    if Y == 'e':
        pause()
    return

#--Guard Movement AI--
def AI():
    global guards, guard1, guard2, guard3, guard4
    for guard in guards:
        direction = random.randint(1,4)
        if direction == 1 and guard.y > 1:
            guard.y -= 1
        if direction == 2 and guard.x < gridSize.x-2:
            guard.x += 1
        if direction == 3 and guard.y < gridSize.y-2:
            guard.y += 1
        if direction == 4 and guard.x > 0:
            guard.x -= 1

def new_round():
    global door, player, guards, guard1, guard2, guard3, guard4, lifeOrb, li
    door = random.randint(1,gridSize.y-2)
    player = Game_Object(0,random.randint(1,gridSize.y-2))
    guard1 = Game_Object(random.randint(2,gridSize.x-2),random.randint(1,gridSize.y-2))
    guard2 = Game_Object(random.randint(2,gridSize.x-2),random.randint(1,gridSize.y-2))
    guard3 = Game_Object(random.randint(2,gridSize.x-2),random.randint(1,gridSize.y-2))
    guard4 = Game_Object(random.randint(2,gridSize.x-2),random.randint(1,gridSize.y-2))
    guards = [guard1, guard2, guard3, guard4]
    lifeOrb = Game_Object(random.randint(2,gridSize.x-2),random.randint(1,gridSize.y-2))
    for guard in guards:
        if lifeOrb.y == guard.y and lifeOrb.x == guard.x:
            lifeOrb = Game_Object(random.randint(2,gridSize.x-2),random.randint(1,gridSize.y-2))
    li = True
    grid()
    return

def life():
    global lifeCount
    lifeCount += 1
    if lifeCount > 10:
        lifeCount = 10
    return

def life_2():
    global lifeOrb, li
    lifeOrb.y = gridSize.y-1
    lifeOrb.x = gridSize.x-1
    li = False
    grid()
    return

def end_round():
    global lifeCount
    lifeCount -= 1
    if lifeCount == 0:
        end_game()
    else:
        new_round()
    return

def end_game():
    global game, menu, sv
    if sv == True:
        os.remove('resources/data/svdta.pickle')
    clear()
    update_highscore()
    print('Game Over\nScore =',score,'\nPress "H" to view highscores')
    a = input()
    if a == 'H' or a == 'h':
        highscore()
    else:
        pass
    game = False
    menu = True
    return

def highscore():
    with open('resources/data/highscore.pickle', 'rb') as g:
        hscore1, hscore2, hscore3, hscore4, hscore5, hscore6 = pickle.load(g)
    print('Highscore\n','\n1:',hscore1,'\n2:',hscore2,'\n3:',hscore3,'\n4:',hscore4,'\n5:',hscore5,'\n6:',hscore6)
    input()
    return

def update_highscore():
    with open('resources/data/highscore.pickle', 'rb') as g:
        hscore1, hscore2, hscore3, hscore4, hscore5, hscore6 = pickle.load(g)
    if score > hscore1:
        hscore6 = hscore5
        hscore5 = hscore4
        hscore4 = hscore3
        hscore3 = hscore2
        hscore2 = hscore1
        hscore1 = score
    elif score > hscore2:
        hscore6 = hscore5
        hscore5 = hscore4
        hscore4 = hscore3
        hscore3 = hscore2
        hscore2 = score
    elif score > hscore3:
        hscore6 = hscore5
        hscore5 = hscore4
        hscore4 = hscore3
        hscore3 = score
    elif score > hscore4:
        hscore6 = hscore5
        hscore5 = hscore4
        hscore4 = score
    elif score > hscore5:
        hscore6 = hscore5
        hscore5 = score
    elif score > hscore6:
        hscore6 = score
    else:
        pass
    with open('resources/data/highscore.pickle', 'wb') as g:
        pickle.dump([hscore1, hscore2, hscore3, hscore4, hscore5, hscore6], g)
        
def pause():
    global game, menu
    pause = True
    while pause == True:
        clear()
        print('Type the number of an option.\n\n1: Return to Game\n2: Save\n3: Main Menu')
        n = input()
        if n == '1':
            pause = False
        if n == '2':
            clear()
            print('WARNING: Saving will overwrite the last save game\nWould you still like to save the game?\n1: Yes\n2. No')
            s = input()
            if s == '1':
                with open('resources/data/svdta.pickle', 'wb') as f:
                    pickle.dump([gridSize, score, lifeCount, lifeOrb, player, guards, guard1, guard2, guard3, guard4, door], f)
                clear()
                print('Save Complete')
                input()
            if s == '2':
                pass
        if n == '3':
            pause = False
            menu = True
            game = False
    clear()
    n = False
    grid()
    return

def Settings():
    global gridSize
    settings = True
    while settings == True:
        clear()
        print('Settings\n\nType the number of an option.\n\n1: Change grid length\n2: Change grid height')
        if op_sys == 'Windows':
            print('3: Change Color\n4: Back')
        if op_sys != 'Windows':
            print('3: Back')
        o = input()
        clear()
        if o == '1':
            print('Enter a new length\nCurrent length', gridSize.x)
            try:
                xnew = int(input())
            except ValueError:
                xnew = gridSize.x
            if xnew < 10:
                if xnew > 4:
                    print('WARNING: This grid size might not be playable')
                    input()
                if xnew < 5:
                    print('Entered value is to small. Length set to 10')
                    xnew = 10
                    input()
            gridSize.x = xnew
        if o == '2':
            gridSize.y -= 2
            print('Enter a new height\nCurrent height', gridSize.y)
            try:
                ynew = int(input())
            except ValueError:
                ynew = gridSize.y
            if ynew < 8:
                if ynew > 4:
                    print('WARNING: This grid size might not be playable')
                    input()
                if ynew < 5:
                    print('Entered value is to small. Height set to 10')
                    ynew = 8
                    input()
            gridSize.y = ynew + 2
        if o == '3' and op_sys == 'Windows':
            print('Pick a new color\nColors\n0 = Black       8 = Gray\n1 = Blue        9 = Light Blue\n2 = Green       A = Light Green\n3 = Aqua        B = Light Aqua\n4 = Red         C = Light Red\n5 = Purple      D = Light Purple\n6 = Yellow      E = Light Yellow\n7 = White       F = Bright White\nEntering anything other than one of the colors listed will set colors to default')
            color_list = ['1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','A','B','C','D','E','F']
            print('Background Color')
            color.x = input()
            if color.x not in color_list:
                color.x = '0'
            print('Text Color')
            color.y = input()
            if color.y not in color_list:
                color.y = '7'
            if color.x == color.y:
                color.x = '0'
                color.y = '7'
            os.system('color ' + color.x + color.y)
        if o == '3' and op_sys != 'Windows':
            settings = False
        if o == '4' and op_sys == 'Windows':
            settings = False
    with open('resources/data/config.pickle', 'wb') as config:
                    pickle.dump([gridSize, color], config)
    return

#--master loop--
with open('resources/data/config.pickle', 'rb') as config:
    gridSize, color = pickle.load(config)
os.system('color ' + color.x + color.y)
master = True
menu = True
game = False
while master == True:
    #--menu loop--
    while menu == True:
        clear()
        print('Type the number of an option.\n\n1: New Game\n2: Load Game\n3: Highscore\n4: Instructions\n5: Settings\n6: Quit')
        m = input()
        clear()
        if m == '1':
            menu = False
            game = True
            sv = False
            lifeCount = 1
            score = 0
            new_round()
        if m == '2':
            loaderror = False
            try:
                with open('resources/data/svdta.pickle', 'rb') as svdta:
                    gridSize, score, lifeCount, lifeOrb, player, guards, guard1, guard2, guard3, guard4, door = pickle.load(svdta)
                menu = False
                game = True
                li = True
                sv = True
                grid()
            except FileNotFoundError:
                print('No save data found')
                input()
        if m == '3':
            highscore()
        if m == '4':
            print('Instructions\n\nGet your person (i) to the exit (})\nwithout getting caught by the guards (#).\n(*) will give you +1 life.\nUse the \'w\',\'a\',\'s\',\'d\' keys to move your character.\nUse the \'e\' key to open the pause menu.')
            input()
        if m == '5':
            Settings()
        if m == '6':
            master = False
            menu = False
            game = False

    #--game loop--
    while game == True:
        n = True
        Player()
        if n == True:
            AI()
            grid()
        if player.y == door and player.x == gridSize.x-1:
            score += 1
            new_round()
        if player.y == lifeOrb.y and player.x == lifeOrb.x:
            life()
            life_2()
        for guard in guards:
            if lifeOrb.y == guard.y and lifeOrb.x == guard.x:
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
