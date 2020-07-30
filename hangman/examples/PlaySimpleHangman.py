"""Simple example of using HangmanGame."""

from hangman import HangmanGame


print('\n\nH A N G M A N\n')

# Create the game.
game = HangmanGame()

game.set_word()
game_over = not game.get_status() == 'guessing'

# Loop while the player is guessing.
while not game_over:
    print(game.get_hangman())
    print(game.get_position())
    game.guess_letter()
    game_over = not game.get_status() == 'guessing'

print(game.get_hangman())
print(game.get_position())

# Messages for the player post-game.
if game.get_status() == 'won':
    print('Congratulations! You guessed the word correctly.')
else:
    print(f'The word is: {game.get_word()}')
    print('I am sure you will do better next time. :)')

print('\nThanks for playing!')
print('We\'ll see how well you did in the next stage\n')
