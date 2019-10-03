# This file manages saving and loading games.

import sqlite3

from resources.classes.Game import Game as Game
from resources.classes.GameElement import GameElement as GameElement

import resources.tools.helpers as helpers


def insert_game_elements(game, save_id):
    database = sqlite3.connect('resources/data/escape.db')
    cursor = database.cursor()
    cursor.execute('''insert into game_elements (name,save_id,x_coordinate,y_coordinate)
                    values (?,?,?,?);''', ("player", save_id, game.player.x, game.player.y))
    cursor.execute('''insert into game_elements (name,save_id,x_coordinate,y_coordinate)
                    values (?,?,?,?);''', ("door", save_id, game.grid_size.x - 1, game.door))
    cursor.execute('''insert into game_elements (name,save_id,x_coordinate,y_coordinate)
                    values (?,?,?,?);''', ("life_orb", save_id, game.life_orb.x, game.life_orb.y))
    for guard in game.guards:
        cursor.execute('''insert into game_elements (name,save_id,x_coordinate,y_coordinate) 
                        values (?,?,?,?);''', ("guard", save_id, guard.x, guard.y))
    database.commit()
    database.close()
    return


def insert_save(game, save_name):
    try:
        database = sqlite3.connect('resources/data/escape.db')
        cursor = database.cursor()
        cursor.execute('''insert into save_data (difficulty,"length",life_orb_active,lives,name,score,width) 
                        values (?,?,?,?,?,?,?);''',
                       (game.difficulty, game.grid_size.x, str(game.life_orb_active),
                        game.lives, save_name, game.score, game.grid_size.y))
        database.commit()
        database.close()
        save_id = cursor.lastrowid
        insert_game_elements(game, save_id)
        game.id = save_id
        return True, game
    except sqlite3.OperationalError:
        return False, game


def update_game_elements(game, save_id):
    database = sqlite3.connect('resources/data/escape.db')
    cursor = database.cursor()
    cursor.execute('''delete from game_elements where save_id = {save_id}'''.format(save_id=save_id))
    database.commit()
    database.close()
    insert_game_elements(game, save_id)
    return


def update_save(game):
    try:
        database = sqlite3.connect('resources/data/escape.db')
        cursor = database.cursor()
        cursor.execute('''update save_data 
                        set difficulty = ?,"length" = ?,life_orb_active = ?,lives = ?,score = ?,width = ? 
                        where id = ?;''',
                       (game.difficulty, game.grid_size.x, str(game.life_orb_active),
                        game.lives, game.score, game.grid_size.y, game.id))
        database.commit()
        database.close()
        update_game_elements(game, game.id)
        return True
    except sqlite3.OperationalError:
        return False


def delete_save(save_id):
    try:
        database = sqlite3.connect('resources/data/escape.db')
        cursor = database.cursor()
        cursor.execute('''delete from save_data where id = {save_id}'''.format(save_id=save_id))
        cursor.execute('''delete from game_elements where save_id = {save_id}'''.format(save_id=save_id))
        database.commit()
        database.close()
        return True
    except sqlite3.OperationalError:
        return False


def save_game(game):
    helpers.clear()
    if game.id is None:
        print('Name this save file')
        save_name = input()
        success, game = insert_save(game, save_name)
    else:
        success = update_save(game)
    helpers.clear()
    if success:
        input("Game Saved!")
    else:
        input("ERROR: Could not save game data to database.")


def display_saves():
    database = sqlite3.connect('resources/data/escape.db')
    cursor = database.cursor()
    cursor.execute('''select sd.id, sd.name from save_data sd;''')
    result_set = cursor.fetchall()
    database.close()
    if len(result_set) == 0:
        input('No save games found.')
        selected_save = 'NO_SAVE_GAMES'
    else:
        print('Type in the ID of the save file to load.\n')
        print('ID:\tName:')
        for result in result_set:
            save_id, name = result
            print('{id}\t{name}'.format(id=save_id, name=name))
        selected_save = input()
    return selected_save


def load_game():
    selected_save = display_saves()
    if selected_save == "NO_SAVE_GAMES":
        return None
    else:
        try:
            database = sqlite3.connect('resources/data/escape.db')
            cursor = database.cursor()
            cursor.execute('''select * from save_data sd where sd.id = {save_id};'''.format(save_id=int(selected_save)))
            result_set = cursor.fetchall()
            cursor.execute('''select ge.name, ge.x_coordinate, ge.y_coordinate 
                            from game_elements ge where ge.save_id = {save_id};'''.format(save_id=int(selected_save)))
            game_element_result_set = cursor.fetchall()
            database.close()
            if len(result_set) > 0:
                save_id, name, length, width, difficulty, score, lives, life_orb_active = result_set[0]
                game = Game(GameElement(length, width), difficulty, score, lives)
                game.id = save_id
                game.life_orb_active = bool(life_orb_active)
                for game_element in game_element_result_set:
                    name, x, y = game_element
                    if name == 'player':
                        game.player = GameElement(x, y)
                    elif name == 'door':
                        game.door = y
                    elif name == 'life_orb':
                        game.life_orb = GameElement(x, y)
                    elif name == 'guard':
                        game.guards.append(GameElement(x, y))
                return game
            else:
                helpers.clear()
                input('ERROR: No save game found with ID \'{id}\'.'.format(id=selected_save))
                return None
        except sqlite3.OperationalError:
            helpers.clear()
            input('ERROR: Could not load save data from database.')
            return None
        except ValueError:
            helpers.clear()
            input('ERROR: \'{id}\' is not a valid game ID.'.format(id=selected_save))
            return None
