#This tool is used to generate the default config file
#This tool can be used to override an existing config file

import pickle
class Game_Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #color uses the Game_Object class
        #background color = x and forground color = y
def setup():
    print('Generating config.pickle ...')
    gridSize = Game_Object(16, 10)
    color = Game_Object('0', '7')
    with open('../data/config.pickle', 'wb') as config:
        pickle.dump([gridSize, color], config)
    print('Finished generating config.pickle')
    print('Press ENTER to exit')
    input()
if __name__ == '__main__':
    setup()
              
