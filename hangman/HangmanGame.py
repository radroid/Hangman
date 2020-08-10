"""Module contains class HangmanGame."""


from itertools import dropwhile
from time import time
from pathlib import Path


class HangmanGame:
    """Class manages variables and methods required to play hangman.

    Class Attributes:
        file_path (object): PosixPath object defining the location of
                           word_bank.txt.

    Attributes:
        word_bank (set of str): Set of words to be used to play hangman.
        words_played (set of str): A list of words player attempted to guess.
        words_guessed (set of str): A list of words guessed correctly by the
                                    player.
        total_points (int): Keeps a count of the number of points for the
                            player.
        word (str): chosen_word is stored here.
        word_display (list of char): A list of letters in the word.
        guessed_letters (list of char): A list of letters that were guessed by
                                        the player.
        correct_guesses (list of char): A list of letters guessed AND present
                                        in the word.
        incorrect_guesses (list of char): A list of letters guessed AND NOT
                                          present in the word.
        hangman (dict): key - named parts of the hangman, value - named parts
                        of the hangman (updated for incorrect guesses).
        status (str): Stores the state of the game.
        game_number (int): Counts the number of games played.

    """
    file_path = Path.cwd() / 'hangman' / 'data' / 'word_bank.txt'

    def __init__(self, path_to_file=None, ignore_words=None):
        """Initialise GamePlay class.

        Args:
            path_to_file (PosixPath object): PosixPath object containing the
                                             absolute path to .txt file with
                                             words.
            ignore_words (list of words): list of words that are not be ignored
                                          while selecting a word to play.

        """
        if path_to_file is None:
            path_to_file = self.file_path

        self.file_exists(path_to_file)
        self.word_bank = self.save_file_data(path_to_file)

        if ignore_words is None:
            ignore_words = set()

        self.words_played = set(ignore_words)
        self.words_guessed = set()

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

    @classmethod
    def save_file_data(cls, path_to_file):
        """Reads and returns a 'set of strings', containing all the words in
        the .txt file.

        Args:
             path_to_file (PosixPath object): PosixPath object containing the
                                              absolute path to .txt file with
                                              words.

        Returns:
            word_bank (set of str): contains unique set of words
                                    from the .txt file.
        """
        t0 = time()
        words_bank = set()
        with path_to_file.open('r') as f:
            for line in dropwhile(cls.is_comment, f):
                words_bank.add(line.strip())

        duration = round(time() - t0, 5)
        avg_length = round(sum(map(len, words_bank)) / len(words_bank), 2)

        print(f'Word bank is successfully updated.\n'
              f'Filename: {path_to_file}\n'
              f'Time taken to calculate = {duration} s\n'
              f'Total number of words = {len(words_bank)}\n'
              f'Average length of words = {avg_length}\n')

        return words_bank

    @classmethod
    def file_exists(cls, path_to_file):
        """Checks if the filename entered is valid.

        Args:
             path_to_file (PosixPath object): Absolute path to the .txt file.

        Raises:
            TypeError:         If the path is not absolute.
            NameError:         If the path entered doesn't end with the '.txt'.
            FileNotFoundError: If the file is not found in the specified file
                                path.
        """
        if not path_to_file.is_absolute():
            raise TypeError('Please enter the absolute path to the file.')
        elif not path_to_file.suffix == '.txt':
            raise NameError('Please enter the correct path to the .txt file.')
        elif not path_to_file.is_file() and not path_to_file.exists():
            raise FileNotFoundError(f'No file found in: {path_to_file}')

    @staticmethod
    def is_comment(line):
        """Checks if the line provided is a comment, i.e., starts with '#'.

        Args:
             line (str): The line that needs to be checked.

        Returns:
            boolean: whether the line starts with '#' or no.

        """
        return line.startswith('#')

    def update_word_bank(self):
        """Updates word_bank from a new .txt."""
        end = False
        new_filename = ''
        while not end:
            try:
                print('\nEnter "end" if you you want to exit.\n')
                new_filename = input('Enter path to the new .txt file: ')
                if new_filename == 'end':
                    end = True
                else:
                    new_file_path = Path(new_filename)
                    self.file_exists(new_file_path)
                    self.word_bank = self.save_file_data(new_file_path)
                    end = True
            except TypeError as te:
                print(f'Error: {te}')
            except NameError as ne:
                print(f'Error: {ne}')
            except FileNotFoundError as e:
                print(f'Error: {e}')
        print('Loop ended.', end='')
        print('Word bank successfully updated.' if new_filename == 'end'
              else 'Word bank not updated.')

    def set_word(self):
        """Selects a word from a list of words. This word is to be guessed
           in the game."""
        try:
            if len(self.word_bank) == 0:
                raise UserWarning('The word bank has been exhausted. '
                                  'All the words have been used.')

            self.word = self.word_bank.pop()
            self.word_display = ['_' for _ in self.word]
            self.__set_status()

        except UserWarning as error:
            print(f'Error: {error}')
            command = input('Do you want to import words from a new .txt '
                            'file?\n(y/n): ').lower()
            if command == 'y':
                self.update_word_bank()
                self.set_word()
            elif command == 'n':
                raise UserWarning('The word bank has been exhausted and you '
                                  'did not update it.')

    def get_word(self):
        """Returns current word being used in the game."""
        return self.word

    def guess_letter(self):
        """The method updates appropriate variables after an input
           from the console (user)."""
        guess = self.get_valid_guess()
        self.guessed_letters.append(guess)

        if guess in self.word:
            self.correct_guesses.append(guess)
            self.update_word_display(guess)
        else:
            self.incorrect_guesses.append(guess)
            self.update_hangman()

        self.__set_status()

    def get_valid_guess(self):
        """The method takes a single alphabet from the console (user),
           checks if it is not already input and returns it.

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
                print(
                    f'"{guess}" is not a valid input. Please enter a '
                    f'single alphabet.')
            elif not is_new_guess:
                print(
                    f'"{guess}" has already been input before. Please enter '
                    f'a letter not guessed already.')

        return guess.lower()

    def update_word_display(self, guess):
        """Updates the variable responsible for displaying the current position
           of the user (displaying the letters guessed correctly with the
           missing letters of the word).

        Args:
            guess (char): Correctly guessed alphabet.

        Returns: None
        """
        for i, char in enumerate(list(self.word)):
            if guess == char:
                self.word_display[i] = char

    def update_hangman(self):
        """Updates the position of the hangman for every incorrect guess by
           the user."""
        # Symbols to complete hangman's body
        hangman_parts = ['O', '|', '/', '\\', '/', '\\']

        # Index to update the last incorrect guess
        index = len(self.incorrect_guesses) - 1

        # Preparing entry for hangman dictionary update
        update_statement = {
            list(self.hangman.keys())[index]: hangman_parts[index]}

        self.hangman.update(update_statement)

    def get_hangman(self):
        """Returns a string with the current position of the hangman.

        Args: None

        Returns
            hangman (str): Diagram/position of the hangman at
            this point in the game.
        """
        hangman_pole = """
          +---+
          |   |
          |   {head}
          |  {right_hand}{body}{left_hand}
          |  {right_leg} {left_leg}
          |
        =========
        """

        return hangman_pole.format(**self.hangman)

    def get_position(self):
        """Returns a string with the other data needed to play.

        Notes:
            Data includes, word being guessed with missing letter
            replaced with '_' and the letters incorrectly guessed.

            Args: None

            Returns
                string: word with correctly guessed letters and missing letters
                        and incorrectly guessed letters.
        """
        return f'\t {" ".join(self.word_display)}\n' \
               f'Letters guessed: {", ".join(self.guessed_letters)}'

    def update_points(self):
        """Updates the total_points. The points system is slightly complex.
           The rules that govern it are as follows.

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
            You get positive points for correctly guessing the word and
            negative for not being able to guess it.
            Points are based on the letters in the word to be guessed and
            number of incorrect guesses.

            If you correctly guess, i.e. 'won':
            - One point is awarded for every common letter in the word.
            - Two points are awarded for every un-common letter in the word.
            - One point for each guess left. eg. if 3 guesses left, (points+3)

            If you fail to guess the word, i.e. 'lost':
            - First points are awarded based on what you have guessed (same as
              'won')
            - For the letters that were not guess:
             * Two points are deducted for every common letter in the word not
               guessed.
             * One point is deducted for every un-common letter in the word not
               guessed.
            - If the sum of positive and negative points is more than 0,
              points = 0.
            - else negative score is added used.

            Points for individual games are added to total_points.

        Returns:
            points (int): The points scored in this particular round/game.
        """
        list_of_common_char = 'e-t-a-o-i-n-s-h-r-d-l-u'.split('-')
        points = 0

        game_status = self.get_status()

        if game_status == 'won':
            for char in self.correct_guesses:
                points += 1 if (char in list_of_common_char) else 2
            points += len(self.hangman) - len(self.incorrect_guesses)

        elif game_status == 'lost':
            positive_points = 0
            negative_points = 0

            # Creating a set of letters that were not guessed.
            missed_letters = set(self.word).difference(
                set(self.correct_guesses))

            for char in missed_letters:
                negative_points += 2 if (char in list_of_common_char) else 1
            for char in self.correct_guesses:
                positive_points += 1 if (char in list_of_common_char) else 2
            points = 0 if positive_points >= negative_points else (
                        positive_points - negative_points)

        self.total_points += points

        return points

    def get_total_points(self):
        """Returns the total_points of all the games played till now.

        Args: None
        Returns: total_points (int) - Number of points scored by the player
                                      till now.
        """
        return self.total_points

    def __set_status(self):
        """Updates the status of the game if ended."""
        if len(self.incorrect_guesses) >= len(self.hangman):
            self.status = 'lost'
        elif self.word == ''.join(self.word_display):
            self.status = 'won'
        else:
            self.status = 'guessing'

    def get_status(self):
        """Returns the status of the game.

        Args: None
        Returns: status (str) - 'won', 'lost' or 'guessing'
        """
        self.__set_status()
        return self.status

    def __update_list_of_words(self):
        """Adds the word played to a set containing all the words played t
           ill now.

        If the word is correctly guessed, the word is also added to another
        set containing correctly guessed words.
         """
        self.words_played.add(self.word)
        if self.status == 'won':
            self.words_guessed.add(self.word)

    def reset_game(self):
        """Resets all the variables related to the specific round, if the
           game is over."""
        if not self.get_status() == 'guessing':
            self.__update_list_of_words()

            self.word = ''
            self.word_display = []
            self.guessed_letters = []
            self.correct_guesses = []
            self.incorrect_guesses = []
            self.hangman = {'head': ' ', 'body': ' ', 'right_hand': ' ',
                            'left_hand': ' ', 'right_leg': ' ',
                            'left_leg': ' '}
            self.status = ''
            self.game_number = len(self.words_played) + 1

    def __repr__(self):
        """Prints the total points and words guessed by the player."""
        print(f'\n\nTotal points: {self.get_total_points()}\n'
              f'Words correctly guessed: {", ".join(self.words_guessed)}\n\n')
