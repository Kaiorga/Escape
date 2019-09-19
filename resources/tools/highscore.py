# This tool is used to generate and update highscores.

import pickle


def setup(location):
    highscores = []
    player_names = []
    with open(location, 'wb') as f:
        pickle.dump([highscores, player_names], f)
    return


def display(grid_size, difficulty):
    try:
        with open('resources/data/highscore-x{x}y{y}d{difficulty}.pickle'.format(x=grid_size.x, y=grid_size.y - 2,
                                                                                 difficulty=difficulty), 'rb') as f:
            highscores, player_names = pickle.load(f)
    except FileNotFoundError:
        setup('resources/data/highscore-x{x}y{y}d{difficulty}.pickle'.format(x=grid_size.x, y=grid_size.y - 2,
                                                                             difficulty=difficulty))
        with open('resources/data/highscore-x{x}y{y}d{difficulty}.pickle'.format(x=grid_size.x, y=grid_size.y - 2,
                                                                                 difficulty=difficulty), 'rb') as f:
            highscores, player_names = pickle.load(f)
    print(
        'Highscores for grid size {x},{y}\nDifficulty setting: {difficulty}\n'.format(x=grid_size.x, y=grid_size.y - 2,
                                                                                      difficulty=difficulty * 100))
    if len(highscores) == 0:
        print('No scores to show')
    else:
        index = 0
        print('Rank\tScore\tName')
        while index < len(highscores):
            print('{rank}:\t{score}\t{name}'.format(rank=index + 1, score=highscores[index], name=player_names[index]))
            index += 1
    input()
    return


def update(score, player, grid_size, difficulty):
    try:
        with open('resources/data/highscore-x{x}y{y}d{difficulty}.pickle'.format(x=grid_size.x, y=grid_size.y - 2,
                                                                                 difficulty=difficulty), 'rb') as f:
            highscores, player_names = pickle.load(f)
    except FileNotFoundError:
        setup('resources/data/highscore-x{x}y{y}d{difficulty}.pickle'.format(x=grid_size.x, y=grid_size.y - 2,
                                                                             difficulty=difficulty))
        with open('resources/data/highscore-x{x}y{y}d{difficulty}.pickle'.format(x=grid_size.x, y=grid_size.y - 2,
                                                                                 difficulty=difficulty), 'rb') as f:
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
            index += 1
        if index == len(highscores):
            highscores.append(score)
            player_names.append(player)
    with open('resources/data/highscore-x{x}y{y}d{difficulty}.pickle'.format(x=grid_size.x, y=grid_size.y - 2,
                                                                             difficulty=difficulty), 'wb') as f:
        pickle.dump([highscores, player_names], f)
    return
