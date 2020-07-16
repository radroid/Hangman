import random as r
from itertools import dropwhile
from time import time
from os import path,getcwd


class HangmanGame:
    """
    HangmanGame class manages variables and methods required to play Hangman.

    Attributes:
        filename (str): Path to file containing the word bank.
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
        status (str): Stores the state of the game.
        game_number (int): Counts the number of games played.
    """

    def __init__(self, filename=None, words_played=None, words_guessed=None):
        """
        Initialise GamePlay class.

        Args:
            filename (str): Path to file containing the word bank.
             words_played (set of str): number of words already played.
             words_guessed (set of str): number of words guessed correctly out of the words played.

        """

        if filename is None:
            filename = path.dirname(__file__) + '/src/word_bank.txt'

        self.is_valid_filename(filename)
        self.filename = filename

        if words_guessed is None:
            words_guessed = set({})
        if words_played is None:
            words_played = set({})

        self.words_played = words_played
        self.words_guessed = words_guessed

        self.total_points = 0
        self.word = ''

        self.word_display = []
        self.guessed_letters = []
        self.correct_guesses = []
        self.incorrect_guesses = []
        self.hangman = {'head': ' ', 'body': ' ', 'right_hand': ' ',
                        'left_hand': ' ', 'right_leg': ' ', 'left_leg': ' '}

        self.status = ''
        self.game_number = len(self.words_played) + 1

    @staticmethod
    def is_valid_filename(filename):
        """ Checks if the filename entered is valid """
        if not filename.endswith('.txt'):
            raise NameError('Please enter the correct path to the .txt file.')
        elif not path.isfile(filename):
            raise FileNotFoundError(f'No file found in: {filename}')

        HangmanGame.print_file_stats(filename)

    @staticmethod
    def print_file_stats(filename):
        # TODO: Themes and levels can be added.
        """
        Reads a .txt file containing all the words, and returns a list containing them.

        Args:
            filename (str): contains the path to the .txt file that contains the words to be played

        Returns: none
        """
        t0 = time()
        words_bank = []
        with open(filename, 'r') as f:
            for line in dropwhile(HangmanGame.is_comment, f):
                words_bank.append(line)

        duration = round(time() - t0, 5)
        avg_length = round(sum(map(len, words_bank)) / len(words_bank), 2)

        print(f'Filename: {filename}')
        print(f'Time taken to calculate = {duration} s')
        print(f'Total number of words = {len(words_bank)}')
        print(f'Average length of words = {avg_length}\n')

    @staticmethod
    def is_comment(line):
        """
        Checks if the line provided is a comment or no, i.e., starts with '#'

        Args:
             line (str): The line that needs to be checked.

        Returns:
            boolean: whether the line starts with '#' or no.

        """
        return line.startswith('#')

    def set_new_filename(self):
        """ Helps set up a new file for the word bank. """
        while True:
            try:
                new_filename = input('Enter path to/name of the new .txt file: ')
                self.is_valid_filename(new_filename)
                self.print_file_stats(new_filename)
                self.filename = new_filename
                break
            except NameError as e:
                print(f'Error: {e}')
            except FileNotFoundError as e:
                print(f'Error: {e}')

    def set_word(self):
        """ Selects a word from a list of words. This word is to be guessed in the game. """
        try:
            word_bank = []
            with open(self.filename, 'r') as f:
                for word in dropwhile(HangmanGame.is_comment, f):
                    word_bank.append(word)

            # Remove words that have already been guessed.
            word_bank = list(set(word_bank) - set(self.words_played))
            if len(word_bank) == 0:
                raise UserWarning('The word bank input by you is exhausted.')

            # Set the word to be guessed in this round.
            self.word = word_bank[r.randint(0, len(word_bank) - 1)]
            self.word_display = ['_' for _ in self.word]
            self.set_status()

        except UserWarning as error:
            print(f'Error: {error}')

    def get_word(self):
        return self.word

    def guess_letter(self):
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

            # Check if the input is a single character and an alphabet.
            is_valid = len(guess) == 1 and guess.isalpha()

            # Check if the alphabet is already guessed.
            is_new_guess = guess not in self.guessed_letters

            if not is_valid:
                print(f'"{guess}" is not a valid input. Please enter a single alphabet.')
            elif not is_new_guess:
                print(f'"{guess}" has already been input before. Please enter a letter not guessed already.')

        return guess.lower()

    def update_word_display(self, guess):
        """
        Updates the variable responsible for displaying the current position of the user (displaying the letters
        guessed correctly with the missing letters of the word).

        Args:
            guess (char): Correctly guessed alphabet.

        Returns: None
        """

        for i, char in enumerate(list(self.word)):
            if guess == char:
                self.word_display[i] = char

    def update_hangman(self):
        """ Updates the position of the hangman for every incorrect guess by the user """
        hangman_parts = ['O', '|', '/', '\\', '/', '\\']  # Symbols to complete hangman's body
        index = len(self.incorrect_guesses) - 1  # Index to update the last incorrect guess
        update_statement = {list(self.hangman.keys())[index]: hangman_parts[index]}  # Preparing entry for update
        self.hangman.update(update_statement)

    def print_hangman(self):
        # TODO: improve method to make printing to console more modular and flexible
        # TODO: separate hangman art from word.
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
        """
        Updates the total_points. The points system is slightly complex. The rules that govern it are as follows:

        Summary:
            For every letter:
            +1 = common guessed
            -2 = common not guessed (only if 'lost')
            +2 = un-common guessed
            -1 = un-common not guessed (only if 'lost')
            +1 = every un-used guess. (only if 'won')

            overall:
                'won' -> positive
                'lost' -> max 0 or negative

        Notes:
            You get positive points for correctly guessing the word and negative for not being able to guess it.
            Points are based on the letters in the word to be guessed and number of incorrect guesses.

            If you correctly guess, i.e. 'won':
            - One point is awarded for every common letter in the word.
            - Two points are awarded for every un-common letter in the word.
            - One point for each guess left. eg. if 3 guesses left, (points+3)

            If you fail to guess the word, i.e. 'lost':
            - First points are awarded based on what you have guessed (same as 'won')
            - For the letters that were not guess:
             * Two points are deducted for every common letter in the word not guessed.
             * One point is deducted for every un-common letter in the word not guessed.
            - If the sum of positive and negative points is more than 0, points = 0.
            - else negative score is added used.

            Points for individual games are added to total_points.

        """

        list_of_common_char = 'e-t-a-o-i-n-s-h-r-d-l-u'.split('-')
        points = 0
        self.set_status()

        if self.get_status() == 'won':
            for char in self.correct_guesses:
                points += 1 if (char in list_of_common_char) else 2
            points += len(self.hangman) - len(self.incorrect_guesses)

        elif self.get_status() == 'lost':
            positive_points = 0
            negative_points = 0

            # Creating a set of letters that were not guessed.
            missed_letters = set(self.word).difference(set(self.correct_guesses))

            for char in missed_letters:
                negative_points += 2 if (char in list_of_common_char) else 1
            for char in self.correct_guesses:
                positive_points += 1 if (char in list_of_common_char) else 2
            points = 0 if positive_points >= negative_points else (positive_points - negative_points)

        self.total_points += points

        return points

    def get_total_points(self):
        """
        Returns the total_points of all the games played till now.

        Args: None
        Returns: total_points (int) - Number of points scored by the player till now.
        """
        return self.total_points

    def set_status(self):
        """ Updates the status of the game if ended. """

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

    def __update_list_of_words(self):
        """
        Adds the word played to a set containing all the words played till now.
        If the word is correctly guessed, the word is also added to another set containing
        correctly guessed words.
         """
        self.words_played.add(self.word)
        if self.status == 'won':
            self.words_guessed.add(self.word)

    def reset_game(self):
        """ Resets all the variables related to the specific round, if the game is over. """
        if not self.get_status() == 'guessing':

            self.__update_list_of_words()

            self.word = ''
            self.word_display = []
            self.guessed_letters = []
            self.correct_guesses = []
            self.incorrect_guesses = []
            self.hangman = {'head': ' ', 'body': ' ', 'right_hand': ' ',
                            'left_hand': ' ', 'right_leg': ' ', 'left_leg': ' '}
            self.status = ''
            self.game_number = len(self.words_played) + 1

    @classmethod
    def increment_game_object_number(cls):
        cls.game_object_number += 1

    @classmethod
    def get_number_of_games_created(cls):
        return cls.game_object_number
