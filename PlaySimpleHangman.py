from Hangman import HangmanGame


print('\n\nH A N G M A N\n')

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
        print(f'The word is: {game.get_word()}')
        print('I am sure you will do better next time. :)')

    print(f'\nPoints scored in this round: {game.update_points()}')
    print(f'Total points: {game.total_points}\n')
    end_game = input('Would you like to play again? (Y/N) ').lower() == 'n'
    game.reset_game()

print('\n\nThanks for playing!')
print('We\'ll see how well you did in the next stage\n')
