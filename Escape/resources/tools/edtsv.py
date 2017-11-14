#This tool is used for testing
#This tool may corrupt your save data
#Use at your own risk

import os
import pickle
import platform

os.system('title Edit Save')
op_sys = platform.system()

class Game_Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def clear():
    if op_sys == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    return

print('Open Save File\nPress ENTER to open default location')
save = input()
if save == '':
    save = '../data/svdta.pickle'

try:
    with open(save, 'rb') as f:
        gridSize, score, lifeCount, lifeOrb, player, guards, guard1, guard2, guard3, guard4, door = pickle.load(f)
    a = True

except FileNotFoundError:
    print('ERROR: No save data found.\nPress ENTER to continue.')
    input()
    a = False

except PermissionError:
    print('ERROR: No save data found.\nPress ENTER to continue.')
    input()
    a = False

except ValueError:
    print('ERROR: pickle file not compatable.\nPress ENTER to continue.')
    input()
    a = False
    
while a == True:
    clear()
    print('Current save data\n             .x , .y')
    print('gridSize    ',gridSize.x,',',gridSize.y,'\nplayer      ',player.x,',',player.y,'\nguard1      ',guard1.x,',',guard1.y,'\nguard2      ',guard2.x,',',guard2.y,'\nguard3      ',guard3.x,',',guard3.y,'\nguard4      ',guard4.x,',',guard4.y,'\nlifeOrb     ',lifeOrb.x,',',lifeOrb.y,'\nscore       ',score,'\nlifeCount   ',lifeCount,'\ndoor        ',door)
    b = input()
    if b == '~exit':
        a = False
    if b == '~save':
        with open(save, 'wb') as f:
            pickle.dump([gridSize, score, lifeCount, lifeOrb, player, guards, guard1, guard2, guard3, guard4, door], f)
    if b == '~edit':
        print('Choose Variable')
        c = input()
        variables = ['xval','yval','score','lifeCount','lifeOrb.x','lifeOrb.y','player.x','player.y','guard1.x','guard1.y','guard2.x','guard2.y','guard3.x','guard3.y','guard4.x','guard4.y','door']
        if c in variables:
            print('Enter new value')
            try:
                d = int(input())
            except ValueError:
                print('ERROR: Invalid Value for Variable')
                d = 'na'
                input()
            exec("%s = %d" % (c,d))
        else:
            print('ERROR: Invalid Variable')
            input()
    clear()
