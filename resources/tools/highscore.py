# This tool is used to generate and update highscores.

import sqlite3

import resources.tools.helpers as helpers


def display(grid_size, difficulty):
    database = sqlite3.connect('resources/data/escape.db')
    cursor = database.cursor()
    cursor.execute('''select h.name, h.score from highscores h 
                    where h."length" = {length} and h.width = {width} and h.difficulty = {difficulty} 
                    order by h.score desc;'''
                   .format(length=grid_size.x, width=grid_size.y, difficulty=difficulty))
    result_set = cursor.fetchall()
    database.close()
    print('Highscores for {x}x{y} grid and difficulty setting {difficulty}\n'
          .format(x=grid_size.x, y=grid_size.y - 2, difficulty=difficulty * 100))
    if len(result_set) == 0:
        print('No scores to show')
    else:
        index = 1
        print('Rank\tScore\tName')
        for result in result_set:
            player_name, score = result
            print('{rank}:\t{score}\t{name}'.format(rank=index, score=score, name=player_name))
            index += 1
    input()
    return


def update(score, player, grid_size, difficulty):
    try:
        database = sqlite3.connect('resources/data/escape.db')
        cursor = database.cursor()
        cursor.execute('''insert into highscores(length, width, difficulty, name, score) 
                        values(?, ?, ?, ?, ?)''', (grid_size.x, grid_size.y, difficulty, player, score))
        database.commit()
        database.close()
        option = helpers.get_input('Press "H" to view highscores')
        helpers.clear()
        if option == 'H' or option == 'h':
            display(grid_size, difficulty)
    except sqlite3.OperationalError:
        helpers.clear()
        print('ERROR: Could not save highscore data to database')
        input()
    return
