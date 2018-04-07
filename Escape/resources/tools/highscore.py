# This tool is used to generate highscore.pickle
# This tool can be used to override an existing highscore.pickle

import pickle


def setup(location, message):
    print('Creating highscore.pickle...')
    highscores = []
    with open(location, 'wb') as f:
        pickle.dump(highscores, f)
    print('Finished creating highscore.pickle')
    print('Press ENTER to ' + message)
    input()
    return


def display():
    try:
        with open('resources/data/highscore.pickle', 'rb') as highscore:
            highscores = pickle.load(highscore)
    except FileNotFoundError:
        setup('resources/data/highscore.pickle', 'continue')
        with open('resources/data/highscore.pickle', 'rb') as highscore:
            highscores = pickle.load(highscore)
    if len(highscores) == 0:
        print('No scores to show')
    else:
        index = 0
        while index < len(highscores):
            print('{rank}: {score}'.format(rank=index+1, score=highscores[index]))
            index +=1
    input()
    return


def update(score):
    try:
        with open('resources/data/highscore.pickle', 'rb') as f:
            highscores = pickle.load(f)
    except FileNotFoundError:
        setup('resources/data/highscore.pickle', 'continue')
        with open('resources/data/highscore.pickle', 'rb') as f:
            highscores = pickle.load(f)
    if len(highscores) == 0:
        highscores.append(score)
    else:
        index = 0
        while index < len(highscores):
            if score > highscores[index]:
                highscores.insert(index, score)
                break
            index +=1
        if index == len(highscores):
            highscores.append(score)
    with open('resources/data/highscore.pickle', 'wb') as f:
        pickle.dump(highscores, f)
    return


if __name__ == '__main__':
    setup('../data/highscore.pickle', 'exit')
