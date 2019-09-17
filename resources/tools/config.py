# This tool is used to generate the default config file

import pickle


class GameObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # color uses the Game_Object class
        # background color = x and foreground color = y


def setup(location):
    print('Could not find config file\nGenerating new config file ...')
    grid_size = GameObject(16, 10)
    color = GameObject('0', '7')
    controls = {'up': 'w', 'left': 'a', 'down': 's', 'right': 'd', 'pause': 'e'}
    difficulty = 0.03125
    with open(location, 'wb') as file:
        pickle.dump([grid_size, color, controls, difficulty], file)
    input('Finished generating config file\nPress ENTER to continue')
    return
