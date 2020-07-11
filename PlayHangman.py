from hangman_pack import HangmanGame

print('\n\nH A N G M A N\n')

game = HangmanGame()
game.set_word()
status = game.get_status() == 'guessing'

while status:
    game.print_hangman()
    game.guess_letter()
    status = game.get_status() == 'guessing'

game.print_hangman()

if status == 'won':
    print('Congratulations! You guessed the word correctly.')
else:
    print('Better luck next time. :(')

print(f'\nPoints scored: {game.update_points()}')

print("\n\nThanks for playing!")
print("We'll see how well you did in the next stage")
