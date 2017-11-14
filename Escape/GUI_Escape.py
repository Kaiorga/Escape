#Version X.0.0 - The GUI Update
#Escape by TyReesh Boedhram
#NOTE: This game must be run in Command Prompt on Windows or Terminal in Linux to work properly.
#This game will not work properly on Sololearn or in IDLE.
#Not tested on Mac OSX yet.
#Please report any bugs.

import os
import tkinter
import pickle
import random
import platform

'''
os.system('@echo off')
os.system('title Escape')
op_sys = platform.system()

def clear():
    if op_sys == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    return

def grid():
    global matrix, li
    clear()
    matrix = [[ ' ' for x in range(xval)] for y in range(yval)]
    for sublist in matrix:
        #--top and bottom border--
        g = 0
        while g < xval:
            matrix[0][g] = '-'
            matrix[yval-1][g] = '-'
            g = g + 1
        #--game objects--
        matrix[A][B] = 'i'
        matrix[P][xval-1] = '}'
        matrix[D][E] = '#'
        matrix[F][G] = '#'
        matrix[H][I] = '#'
        matrix[N][O] = '#'
        if li == True:
            matrix[Q][R] = '*'
        else:
            matrix[Q][R] = '-'
        #--removes extra characters--
        s = str(sublist)
        s = s.replace('[', '|').replace(']', '|').replace(',','').replace('\'','')
        print (s)
    print ('Score:',Z,'Lives:',C)
    return

#--Player Commands--
def player():
    global A, B
    Y = input()
    if Y == 'w' and A > 1:
        matrix[A][B] = ' '
        A = A - 1
    if Y == 'a' and B > 0:
        matrix[A][B] = ' '
        B = B - 1
    if Y == 's' and A < yval-2:
        matrix[A][B] = ' '
        A = A + 1
    if Y == 'd' and B < xval-1:
        matrix[A][B] = ' '
        B = B + 1
        if A != P and B == xval-1:
            B = B - 1
    if Y == 'e':
        pause()
    return

#--Guard Movement AI--
def AI():
    global D, E, F, G, H, I, N, O
    J = random.randint(1,4)
    K = random.randint(1,4)
    L = random.randint(1,4)
    M = random.randint(1,4)
    if J == 1 and D > 1:
        matrix[D][E] = ' '
        D = D - 1
    if J == 2 and E < xval-2:
        matrix[D][E] = ' '
        E = E + 1
    if J == 3 and D < yval-2:
        matrix[D][E] = ' '
        D = D + 1
    if J == 4 and E > 0:
        matrix[D][E] = ' '
        E = E - 1
    if K == 1 and F > 1:
        matrix[F][G] = ' '
        F = F - 1
    if K == 2 and G < xval-2:
        matrix[F][G] = ' '
        G = G + 1
    if K == 3 and F < yval-2:
        matrix[F][G] = ' '
        F = F + 1
    if K == 4 and G > 0:
        matrix[F][G] = ' '
        G = G - 1
    if L == 1 and H > 1:
        matrix[H][I] = ' '
        H = H - 1
    if L == 2 and I < xval-2:
        matrix[H][I] = ' '
        I = I + 1
    if L == 3 and H < yval-2:
        matrix[H][I] = ' '
        H = H + 1
    if L == 4 and I > 0:
        matrix[H][I] = ' '
        I = I - 1
    if M == 1 and N > 1:
        matrix[N][O] = ' '
        N = N - 1
    if M == 2 and O < xval-2:
        matrix[N][O] = ' '
        O = O + 1
    if M == 3 and N < yval-2:
        matrix[N][O] = ' '
        N = N + 1
    if M == 4 and O > 0:
        matrix[N][O] = ' '
        O = O - 1
    return

def new_round():
    global P, A, B, D, E, F, G, H, I, N, O, Q, R, li
    P = random.randint(1,yval-2)
    A = 3
    B = 0
    D = random.randint(1,yval-2)
    E = random.randint(2,xval-2)
    F = random.randint(1,yval-2)
    G = random.randint(2,xval-2)
    H = random.randint(1,yval-2)
    I = random.randint(2,xval-2)
    N = random.randint(1,yval-2)
    O = random.randint(2,xval-2)
    Q = random.randint(1,yval-2)
    R = random.randint(2,xval-2)
    if Q == D and R == E:
        Q = random.randint(1,yval-2)
        R = random.randint(2,xval-2)
    if Q == F and R == G:
        Q = random.randint(1,yval-2)
        R = random.randint(2,xval-2)
    if Q == H and R == I:
        Q = random.randint(1,yval-2)
        R = random.randint(2,xval-2)
    if Q == N and R == O:
        Q = random.randint(1,yval-2)
        R = random.randint(2,xval-2)
    li = True
    grid()
    return

def life():
    global C
    C = C + 1
    if C > 10:
        C = 10
    return

def life_2():
    global Q, R, li
    Q = yval-1
    R = xval-1
    li = False
    grid()
    return

def end_round():
    global C
    C = C - 1
    if C == 0:
        end_game()
    if C > 0:
        new_round()
    return

def end_game():
    global game, menu, sv
    if sv == True:
        os.remove('resources/data/svdta.pickle')
    clear()
    update_highscore()
    print('Game Over\nScore =',Z,'\nPress "H" to view highscores')
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
    if Z > hscore1:
        hscore6 = hscore5
        hscore5 = hscore4
        hscore4 = hscore3
        hscore3 = hscore2
        hscore2 = hscore1
        hscore1 = Z
    elif Z > hscore2:
        hscore6 = hscore5
        hscore5 = hscore4
        hscore4 = hscore3
        hscore3 = hscore2
        hscore2 = Z
    elif Z > hscore3:
        hscore6 = hscore5
        hscore5 = hscore4
        hscore4 = hscore3
        hscore3 = Z
    elif Z > hscore4:
        hscore6 = hscore5
        hscore5 = hscore4
        hscore4 = Z
    elif Z > hscore5:
        hscore6 = hscore5
        hscore5 = Z
    elif Z > hscore6:
        hscore6 = Z
    else:
        pass
    with open('resources/data/highscore.pickle', 'wb') as g:
        pickle.dump([hscore1, hscore2, hscore3, hscore4, hscore5, hscore6], g)
        
def pause():
    global game, menu, n
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
                    pickle.dump([A, B, C, D, E, F, G, H, I, N, O, P, Q, R, Z, xval, yval], f)
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
    global xval, yval
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
            print('Enter a new length\nCurrent length', xval)
            try:
                xnew = int(input())
            except ValueError:
                xnew = xval
            if xnew < 10:
                if xnew > 4:
                    print('WARNING: This grid size might not be playable')
                    input()
                if xnew < 5:
                    print('Entered value is to small. Length set to 10')
                    xnew = 10
                    input()
            xval = xnew
        if o == '2':
            yval = yval - 2
            print('Enter a new height\nCurrent height', yval)
            try:
                ynew = int(input())
            except ValueError:
                ynew = yval
            if ynew < 8:
                if ynew > 4:
                    print('WARNING: This grid size might not be playable')
                    input()
                if ynew < 5:
                    print('Entered value is to small. Height set to 10')
                    ynew = 8
                    input()
            yval = ynew + 2
        if o == '3' and op_sys == 'Windows':
            print('Pick a new color\nColors\n0 = Black       8 = Gray\n1 = Blue        9 = Light Blue\n2 = Green       A = Light Green\n3 = Aqua        B = Light Aqua\n4 = Red         C = Light Red\n5 = Purple      D = Light Purple\n6 = Yellow      E = Light Yellow\n7 = White       F = Bright White\nEntering anything other than one of the colors listed will set colors to default')
            color_list = ['1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','A','B','C','D','E','F']
            print('Background Color')
            bg = input()
            if bg not in color_list:
                bg = '0'
            print('Text Color')
            fg = input()
            if fg not in color_list:
                fg = '7'
            if bg == fg:
                bg = '0'
                fg = '7'
            os.system('color ' + bg + fg)
        if o == '3' and op_sys != 'Windows':
            settings = False
        if o == '4' and op_sys == 'Windows':
            settings = False
    return

#--master loop--
xval = 16
yval = 10
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
            C = 1
            Z = 0
            new_round()
        if m == '2':
            loaderror = False
            try:
                with open('resources/data/svdta.pickle', 'rb') as f:
                    A, B, C, D, E, F, G, H, I, N, O, P, Q, R, Z, xval, yval = pickle.load(f)
            except FileNotFoundError:
                print('No save data found')
                input()
                loaderror = True
            if loaderror == False:
                menu = False
                game = True
                li = True
                sv = True
                grid()
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
        player()
        if n == True:
            AI()
            grid()
        if A == P and B == xval-1:
            Z = Z + 1
            new_round()
        if A == Q and B == R:
            life()
            life_2()
        if Q == D and R == E:
            life_2()
        if Q == F and R == G:
            life_2()
        if Q == H and R == I:
            life_2()
        if Q == N and R == O:
            life_2()
        if A == D and B == E:
            end_round()
        if A == D and B == E-1:
            end_round()
        if A == D and B == E+1:
            end_round()
        if A == D-1 and B == E:
            end_round()
        if A == D+1 and B == E:
            end_round()
        if A == F and B == G:
            end_round()
        if A == F and B == G-1:
            end_round()
        if A == F and B == G+1:
            end_round()
        if A == F-1 and B == G:
            end_round()
        if A == F+1 and B == G:
            end_round()
        if A == H and B == I:
            end_round()
        if A == H and B == I-1:
            end_round()
        if A == H and B == I+1:
            end_round()
        if A == H-1 and B == I:
            end_round()
        if A == H+1 and B == I:
            end_round()
        if A == N and B == O:
            end_round()
        if A == N and B == O-1:
            end_round()
        if A == N and B == O+1:
            end_round()
        if A == N-1 and B == O:
            end_round()
        if A == N+1 and B == O:
            end_round()
'''
top = tkinter.Tk()
top.title('Escape')
top.geometry('255x160')
New_Game = tkinter.Button(top, text='New Game')
New_Game.pack()
Load_Game = tkinter.Button(top, text='Load Game')
Load_Game.pack()
Highscore = tkinter.Button(top, text='Highscore')
Highscore.pack()
Instructions = tkinter.Button(top, text='Instructions')
Instructions.pack()
Settings = tkinter.Button(top, text='Settings')
Settings.pack()
Quit = tkinter.Button(top, text='Quit')
Quit.pack()
top.mainloop()
