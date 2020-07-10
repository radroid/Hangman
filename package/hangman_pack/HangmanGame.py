import random as r


class HangmanGame:
    """
    GamePlay class to manage the variables and methods required to play Hangman.

    Attributes:
        game_class_number (class int): Counts the number of classes created (helps identity player).

        words_played (list of str): A list of words player attempted to guess.
        words_guessed (list of str): A list of words guessed correctly by the player.
        total_points (int): Keeps a count of the number of points for the player.
        word (str): chosen_word is stored here.
        word_display (list of char): A list of letters in the word.
        guessed_letters (list of char): A list of letters that were guessed by the player.
        correct_guesses (list of char): A list of letters guessed AND present in the word.
        incorrect_guesses (list of char): A list of letters guessed AND NOT present in the word.
        hangman (dict): key - named parts of the hangman, value - named parts of the hangman
                        (updated for incorrect guesses).
        game_number (int): Stores the game_class_number.
        status (str): Stores the state of the game.
    """

    game_class_number = 0

    def __init__(self):
        """ Initialise GamePlay class. """

        self.words_played = []
        self.words_guessed = []
        self.total_points = 0
        self.word = ''
        self.word_display = []
        self.guessed_letters = []
        self.correct_guesses = []
        self.incorrect_guesses = []
        self.hangman = {'head': ' ', 'body': ' ', 'right_hand': ' ',
                        'left_hand': ' ', 'right_leg': ' ', 'left_leg': ' '}
        self.game_number = HangmanGame.game_class_number
        self.status = ''
        HangmanGame.game_class_number += 1

    def set_word(self):
        # TODO: Improve the method to selects from a .txt file.
        """ Selects a word from a list of words. This word is to be guessed in the game. """

        word_list = ['python', 'java', 'kotlin', 'javascript']
        self.word = word_list[r.randint(0, len(word_list) - 1)]
        self.word_display = ['_' for _ in self.word]
        self.set_status()

    def guess_letter(self):
        # TODO: a method to update guessed_letters, correct_guesses, incorrect_guesses, Hangman.
        """ The method updates appropriate variables after an input from the console (user). """

        guess = self.get_valid_guess()
        self.guessed_letters.append(guess)

        if guess in self.word:
            self.correct_guesses.append(guess)
            self.update_word_display(guess)
        else:
            self.incorrect_guesses.append(guess)
            self.update_hangman()

        self.set_status()

    def get_valid_guess(self):
        # TODO: a method to return a valid guess from user input.
        # TODO: check for blank input.
        """
        The method takes a single alphabet from the console (user), checks if it is not already input and returns it.

        Args: None

        Returns:
            guess (char): A valid input from the console (user).
        """

        is_valid = False
        is_new_guess = False
        guess = ''

        while not is_valid or not is_new_guess:
            guess = input('Input a letter: ').strip()
            is_valid = len(guess) == 1 and guess.isalpha()  # checks if the input is a single character and an alphabet.
            is_new_guess = guess not in self.guessed_letters  # checks if the alphabet is already guessed.

            if not is_valid:
                print(f'{guess} is not a valid input. Please enter a single alphabet.')
            elif not is_new_guess:
                print(f'{guess} has already been input before. Please enter a letter not guessed already.')

        return guess.lower()

    def update_word_display(self, guess):
        """
        Updates the variable responsible for displaying the current position of the user (displaying the letters
        guessed correctly with the missing letters of the word).

        Args:
            guess (char): Correctly guessed alphabet.

        Returns: None
        """
        # TODO: A method that updates the variable word_display after user correctly guesses a letter in the word.

        for i, char in enumerate(list(self.word)):
            if guess == char:
                self.word_display[i] = char

    def update_hangman(self):
        # TODO: Define a method to update the position of hangman, make use of incorrect_guesses
        """ Updates the position of the hangman for every incorrect guess by the user """
        hangman_parts = ['O', '|', '/', '\\', '/', '\\']  # Symbols to complete hangman's body
        index = len(self.incorrect_guesses) - 1           # Index to update the last incorrect guess
        update_statement = {list(self.hangman.keys())[index]: hangman_parts[index]} # Preparing entry for update
        self.hangman.update(update_statement)

    def print_hangman(self):
        # TODO: Define a method to print the current position, i.e. Hangman + half-hidden word
        """ Prints the current position of the hangman. """

        h = self.hangman

        hangman_pole = """
          +---+
          |   |
          |   {}
          |  {}{}{} 
          |  {} {}  
          |
        =========
        """

        print(hangman_pole.format(h.get('head'), h.get('right_hand'), h.get('body'),
                                  h.get('left_hand'), h.get('right_leg'), h.get('left_leg')))
        print('\t' + ' '.join(self.word_display) + '\n')
        print(f'Letters guessed: {", ".join(self.guessed_letters)}')

    def update_points(self):
        # TODO: Define a method to update total_points
        pass

    def update_list_of_words(self):
        # TODO: Define a method to add words to words_played and words_guessed
        pass

    def initialise_all(self):
        """ Resets all the variables """
        # TODO: a method to initialise all variables
        self.__init__()
        pass

    def initialise_guesses(self):
        # TODO: a method to initialise variables before starting the next game
        pass

    def set_status(self):
        """ Updates the state of the game if ended. """

        if len(self.incorrect_guesses) >= len(self.hangman):
            self.status = 'lost'
        elif self.word == ''.join(self.word_display):
            self.status = 'won'
        else:
            self.status = 'guessing'

    def get_status(self):
        """
        Returns the status of the game.

        Args: None
        Returns: status (str) - 'won', 'lost' or 'guessing'
        """
        return self.status

    def get_word(self):
        return self.word


if __name__ == '__main__':
    game = HangmanGame()
    game.set_word()
    game.print_hangman()
    for i in range(10):
        game.guess_letter()
        game.print_hangman()
