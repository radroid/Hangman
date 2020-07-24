from Hangman import HangmanGame
from PyDictionary import PyDictionary
from goslate import Goslate as gs
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

    avail_lang = gs.get_languages()
    fact_name = ['Synonyms', 'Antonyms', 'Translation']

    function_num = 2  # r.randint(0, 3)
    lang_num = r.randint(0, len(avail_lang) - 1)

    dictionary = PyDictionary(game.get_word())
    post_game_word_info = [dictionary.getSynonyms,
                           dictionary.getAntonyms,
                           dictionary.translateTo]

    if function_num == 2:
        fun_fact = post_game_word_info[function_num](avail_lang[lang_num])
    else:
        fun_fact = post_game_word_info[function_num]()[0]
        fun_fact = ', '.join(fun_fact.get(game.get_word()))
    print(f'\nFun fact about the word:\n{fact_name[function_num].capitalize()} - {fun_fact}')

    print(f'\nPoints scored in this round: {game.update_points()}')
    print(f'Total points: {game.total_points}\n')
    end_game = input('Would you like to play again? (Y/N) ').lower() == 'n'
    game.reset_game()

print('\n\nThanks for playing!')
print('We\'ll see how well you did in the next stage\n')
