#This tool is used to generate highscore.pickle
#This tool can be used to override an existing highscore.pickle
import pickle
def setup():
    print('Creating highscore.pickle...')
    hscore1 = 0
    hscore2 = 0
    hscore3 = 0
    hscore4 = 0
    hscore5 = 0
    hscore6 = 0
    with open('../data/highscore.pickle', 'wb') as f:
        pickle.dump([hscore1, hscore2, hscore3, hscore4, hscore5, hscore6],f)
    print('Finished creating highscore.pickle')
    print('Press ENTER to exit')
    input()
if __name__ == '__main__':
    setup()
