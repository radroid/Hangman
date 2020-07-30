"""Slightly more advanced example of using HangmanGame."""

from hangman import HangmanGame
from PyDictionary import PyDictionary
from goslate import Goslate
import random

print('\n\nH A N G M A N\n')
print('Hi there! Let\'s see if you can save the first Hangman\n')

game = HangmanGame()

end_game = False
while not end_game:
    game.set_word()
    game_over = not game.get_status() == 'guessing'

    print(game.get_hangman())
    print(game.get_position())

    while not game_over:
        game.guess_letter()
        print(game.get_hangman())
        print(game.get_position())
        game_over = not game.get_status() == 'guessing'

    if game.get_status() == 'won':
        print('Congratulations! You guessed the word correctly.')
    else:
        print(f'The word to be guessed is: {game.get_word()}')
        print('I am sure you will do better next time. :)\n')

    # This section is different from the other example.
    # It helps the player learn something new about word they did not guess.

    # PyDictionary uses Goslate to translate text. Hence, Goslate is used to
    # get the avialable languages.
    gs = Goslate()
    languages = list(gs.get_languages())

    dictionary = PyDictionary(game.get_word())
    func_dict = {'Synonyms': dictionary.getSynonyms,
                 'Antonyms': dictionary.getAntonyms,
                 'Translation': dictionary.translateTo}

    lang = random.choice(languages)
    func_name = random.choice(list(func_dict.keys()))
    function = func_dict[func_name]

    if func_name == 'Translation':
        fun_fact = function(language=lang)[0]
        func_name = f'{func_name.capitalize()} to {lang}'
    else:
        fun_fact = function()[0]
        fun_fact = ', '.join(fun_fact.get(game.get_word()))
        func_name = func_name.capitalize()

    print(f'\nFun fact about the word:\n{func_name}'
          f' -> {fun_fact}')

    print(f'\nPoints scored in this round: {game.update_points()}')
    print(f'Total points: {game.total_points}\n')

    end_game = True

    # Play one more round.
    for attempts in range(3):
        command = input('Would you like to play again? (y/n) ').lower()
        if command == 'n':
            break
        elif command == 'y':
            end_game = False
            game.reset_game()
            break
        else:
            print('Please enter a valid response. Attempts left: '
                  f'{3 - attempts - 1}\n')

print('\n\nThanks for playing!')
print('We\'ll see how well you did in the next stage\n')
