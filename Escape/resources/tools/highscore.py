#This tool is used to generate highscore.pickle
#This tool can be used to override an existing highscore.pickle

import pickle

def display():
    with open('resources/data/highscore.pickle', 'rb') as highscore:
        hscore1, hscore2, hscore3, hscore4, hscore5, hscore6 = pickle.load(highscore)
    print('Highscore\n','\n1:',hscore1,'\n2:',hscore2,'\n3:',hscore3,'\n4:',hscore4,'\n5:',hscore5,'\n6:',hscore6)
    input()
    return

def update(score):
    with open('resources/data/highscore.pickle', 'rb') as highscore:
        hscore1, hscore2, hscore3, hscore4, hscore5, hscore6 = pickle.load(highscore)
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
    with open('resources/data/highscore.pickle', 'wb') as highscore:
        pickle.dump([hscore1, hscore2, hscore3, hscore4, hscore5, hscore6], highscore)

def setup(location):
    print('Creating highscore.pickle...')
    hscore1 = 0
    hscore2 = 0
    hscore3 = 0
    hscore4 = 0
    hscore5 = 0
    hscore6 = 0
    with open(location, 'wb') as f:
        pickle.dump([hscore1, hscore2, hscore3, hscore4, hscore5, hscore6],f)
    print('Finished creating highscore.pickle')
    print('Press ENTER to exit')
    input()
    
if __name__ == '__main__':
    setup('../data/highscore.pickle')
