# This tool is used to generate highscore.pickle
# This tool can be used to override an existing highscore.pickle

import os
import pickle
import platform
op_sys = platform.system()


def clear():
    if op_sys == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    return


def setup(location, message):
    print('Creating highscore.pickle...')
    highscores = []
    player_names = []
    with open(location, 'wb') as f:
        pickle.dump([highscores, player_names], f)
    print('Finished creating highscore.pickle')
    print('Press ENTER to ' + message)
    input()
    clear()
    return


def display():
    try:
        with open('resources/data/highscore.pickle', 'rb') as f:
            highscores, player_names = pickle.load(f)
    except FileNotFoundError:
        setup('resources/data/highscore.pickle', 'continue')
        with open('resources/data/highscore.pickle', 'rb') as f:
            highscores, player_names = pickle.load(f)
    if len(highscores) == 0:
        print('No scores to show')
    else:
        index = 0
        print('Rank\tScore\tName')
        while index < len(highscores):
            print('{rank}:\t{score}\t{name}'.format(rank=index+1, score=highscores[index], name=player_names[index]))
            index +=1
    input()
    return


def update(score, player):
    try:
        with open('resources/data/highscore.pickle', 'rb') as f:
            highscores, player_names = pickle.load(f)
    except FileNotFoundError:
        setup('resources/data/highscore.pickle', 'continue')
        with open('resources/data/highscore.pickle', 'rb') as f:
            highscores, player_names = pickle.load(f)
    if len(highscores) == 0:
        highscores.append(score)
        player_names.append(player)
    else:
        index = 0
        while index < len(highscores):
            if score > highscores[index]:
                highscores.insert(index, score)
                player_names.insert(index, player)
                break
            index +=1
        if index == len(highscores):
            highscores.append(score)
            player_names.append(player)
    with open('resources/data/highscore.pickle', 'wb') as f:
        pickle.dump([highscores, player_names], f)
    return


if __name__ == '__main__':
    setup('../data/highscore.pickle', 'exit')
