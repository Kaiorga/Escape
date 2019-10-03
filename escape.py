# Version 7.0.0
# Escape by TyReesh Boedhram
# NOTE: This game must be run in Command Prompt on Windows or Terminal on Linux to work properly.
# This game will not work properly in IDLE.
# Not tested on Mac OSX yet.
# Please report any bugs.

import os
import random

from resources.classes.Game import Game as Game
from resources.classes.GameElement import GameElement as GameElement

import resources.tools.config as config
import resources.tools.helpers as helpers
import resources.tools.highscore as highscore
import resources.tools.save as save


def grid(game):
    helpers.clear()
    matrix = [[' ' for _ in range(game.grid_size.x)] for _ in range(game.grid_size.y)]
    #   --top and bottom border--
    column = 0
    while column < game.grid_size.x:
        matrix[0][column] = '-'
        matrix[game.grid_size.y - 1][column] = '-'
        column += 1
    #   --game objects--
    matrix[game.door][game.grid_size.x - 1] = '}'
    matrix[game.player.y][game.player.x] = 'i'
    for guard in game.guards:
        matrix[guard.y][guard.x] = '#'
    if game.life_orb_active:
        matrix[game.life_orb.y][game.life_orb.x] = '*'
    #   --removes extra characters--
    for row in matrix:
        row_string = str(row)
        row_string = row_string.replace('[', '|').replace(']', '|').replace(',', '').replace('\'', '')
        print(row_string)
    print('Score: {score}\tLives: {lives}'.format(score=game.score, lives=game.lives))
    return game


# --Player Commands--
def player_input(game, controls):
    y = helpers.get_input()
    if y == controls['up'] and game.player.y > 1:
        game.player.y -= 1
    if y == controls['left'] and game.player.x > 0:
        game.player.x -= 1
    if y == controls['down'] and game.player.y < game.grid_size.y - 2:
        game.player.y += 1
    if y == controls['right'] and game.player.x < game.grid_size.x - 1:
        game.player.x += 1
        if game.player.y != game.door and game.player.x == game.grid_size.x - 1:
            game.player.x -= 1
    if y == controls['pause']:
        pause_menu(game)
    return game


# --Guard Movement AI--
def ai(game):
    for guard in game.guards:
        direction = random.randint(1, 4)
        if direction == 1 and guard.y > 1:
            guard.y -= 1
        if direction == 2 and guard.x < game.grid_size.x - 2:
            guard.x += 1
        if direction == 3 and guard.y < game.grid_size.y - 2:
            guard.y += 1
        if direction == 4 and guard.x > 0:
            guard.x -= 1
    return game


def new_round(game):
    game.door = random.randint(1, game.grid_size.y - 2)
    game.player = GameElement(0, random.randint(1, game.grid_size.y - 2))
    number_of_guards = round((game.grid_size.x * (game.grid_size.y - 2)) * game.difficulty)
    index = 1
    while index <= number_of_guards:
        new_guard = GameElement(random.randint(2, game.grid_size.x - 2), random.randint(1, game.grid_size.y - 2))
        game.guards.append(new_guard)
        index += 1
    if random.randint(1, 5) == 3:
        game.life_orb_active = True
        game.life_orb = GameElement(random.randint(round(game.grid_size.x / 2), game.grid_size.x - 2),
                                    random.randint(1, game.grid_size.y - 2))
    else:
        game.life_orb = GameElement(game.grid_size.x-1, game.grid_size.y-1)
        game.life_orb_active = False
    game = grid(game)
    return game


def life(game):
    if game.lives <= 10:
        game.lives += 1
    return game


def life_2(game):
    game.life_orb.y = game.grid_size.y - 1
    game.life_orb.x = game.grid_size.x - 1
    game.life_orb_active = False
    game = grid(game)
    return game


def end_round(game):
    game.lives -= 1
    if game.lives == 0:
        end_game(game)
    else:
        new_round(game)
    return game


def end_game(game):
    game.game_over = True
    if game.id is not None:
        save.delete_save(game.id)
    helpers.clear()
    player_name = input('Game Over\nScore: {score}\nEnter a name to go with your score: '.format(score=game.score))
    if player_name == '':
        player_name = '(no name)'
    highscore.update(game.score, player_name, game.grid_size, game.difficulty)
    return game


def pause_menu(game):
    while True:
        helpers.clear()
        option = helpers.get_input('Type the number of an option.\n\n1: Return to Game\n2: Save\n3: Main Menu')
        if option == '1':
            break
        if option == '2':
            save.save_game(game)
        if option == '3':
            game.game_over = True
            break
    helpers.clear()
    game.was_paused = True
    game = grid(game)
    return game


def game_loop(game, controls):
    while True:
        game.was_paused = False
        game = player_input(game, controls)
        if not game.was_paused:
            game = ai(game)
            game = grid(game)
            if game.player.y == game.door and game.player.x == game.grid_size.x - 1:
                game.score += 1
                game = new_round(game)
            if game.life_orb_active and game.player.y == game.life_orb.y and game.player.x == game.life_orb.x:
                game = life(game)
                game = life_2(game)
            for guard in game.guards:
                if game.life_orb_active and game.life_orb.y == guard.y and game.life_orb.x == guard.x:
                    game = life_2(game)
                if game.player.y == guard.y and game.player.x == guard.x:
                    game = end_round(game)
                elif game.player.y == guard.y and game.player.x == guard.x - 1:
                    game = end_round(game)
                elif game.player.y == guard.y and game.player.x == guard.x + 1:
                    game = end_round(game)
                elif game.player.y == guard.y - 1 and game.player.x == guard.x:
                    game = end_round(game)
                elif game.player.y == guard.y + 1 and game.player.x == guard.x:
                    game = end_round(game)
        if game.game_over:
            break


def main():
    grid_size, _, controls, difficulty = config.load_config_file()
    # --menu loop--
    while True:
        helpers.clear()
        option = helpers.get_input('Type the number of an option.\n\n1: New Game\n2: Load Game'
                                   '\n3: Highscore\n4: Instructions\n5: Settings\n6: Quit')
        helpers.clear()
        if option == '1':
            game = Game(grid_size, difficulty, 0, 1)
            game = new_round(game)
            game_loop(game, controls)
        if option == '2':
            game = save.load_game()
            if game is not None:
                game = grid(game)
                game_loop(game, controls)
        if option == '3':
            highscore.display(grid_size, difficulty)
        if option == '4':
            input('Instructions\n\n'
                  'Get your person (i) to the exit ({door})\n'
                  'without getting caught by the guards (#).\n'
                  '(*) will give you +1 life.\n'
                  'Use the \'{up}\',\'{left}\',\'{down}\',\'{right}\' keys to move your character.\n'
                  'Use the \'{pause}\' key to open the pause menu.'.format(door='}', up=controls['up'],
                                                                           left=controls['left'],
                                                                           down=controls['down'],
                                                                           right=controls['right'],
                                                                           pause=controls['pause']))
        if option == '5':
            grid_size, controls, difficulty = config.settings_menu()
        if option == '6':
            break


if __name__ == '__main__':
    if helpers.get_os() == 'Windows':
        os.system('title Escape')
    if not os.path.exists('resources/data/escape.db'):
        config.database_setup()
    main()
