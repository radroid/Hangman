from hangman import HangmanGame
from PyDictionary import PyDictionary
from goslate import Goslate
import random as r

print('\n\nH A N G M A N\n')
print('Hi there! Let\'s start with the game\n')

game = HangmanGame()
end_game = False

while not end_game:
    game.set_word()
    status = game.get_status() == 'guessing'
    while status:
        game.print_hangman()
        game.guess_letter()
        status = game.get_status() == 'guessing'

    game.print_hangman()

    if game.get_status() == 'won':
        print('Congratulations! You guessed the word correctly.')

    else:
        print(f'The word to be guessed is: {game.get_word()}')
        print('I am sure you will do better next time. :)\n')

    gs = Goslate()
    avail_lang = gs.get_languages()

    dictionary = PyDictionary(game.get_word())
    func_dict = {'Synonyms': dictionary.getSynonyms,
                 'Antonyms': dictionary.getAntonyms,
                 'Translation': dictionary.translateTo}

    lang = r.choice(avail_lang)
    func_name = r.choice(list(func_dict.keys()))
    function = func_dict[func_name]

    if func_name == 'Translation':
        fun_fact = function(language=lang)
    else:
        fun_fact = function()
        fun_fact = ', '.join(fun_fact.get(game.get_word()))

    print(f'\nFun fact about the word:\n{func_name.capitalize()}'
          f' - {fun_fact}')

    print(f'\nPoints scored in this round: {game.update_points()}')
    print(f'Total points: {game.total_points}\n')
    end_game = input('Would you like to play again? (Y/N) ').lower() == 'n'
    game.reset_game()

print('\n\nThanks for playing!')
print('We\'ll see how well you did in the next stage\n')
